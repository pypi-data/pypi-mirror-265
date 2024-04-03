# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT 
# WITH UNLIMITED RIGHTS
#
# Grant No.: 80NSSC21K0651
# Grantee Name: Universities Space Research Association
# Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
# Copyright 2024 by Universities Space Research Association (USRA). All rights 
# reserved.
#
# Developed by: Suman Bala
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# This work is a derivative of the Gamma-ray Data Tools (GDT), including the 
# Core and Fermi packages, originally developed by the following:
#
#     William Cleveland and Adam Goldstein
#     Universities Space Research Association
#     Science and Technology Institute
#     https://sti.usra.edu
#     
#     Daniel Kocevski
#     National Aeronautics and Space Administration (NASA)
#     Marshall Space Flight Center
#     Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not 
# use this file except in compliance with the License. You may obtain a copy of 
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
# License for the specific language governing permissions and limitations under 
# the License.
#



import numpy as np
import astropy.units as u
import astropy.coordinates.representation as r
from astropy.coordinates import SkyCoord
from scipy.spatial.transform import Rotation
from gdt.core.coords import SpacecraftAxes
from gdt.core.file import FitsFileContextManager
from gdt.core.coords.spacecraft import SpacecraftFrameModelMixin, SpacecraftStatesModelMixin
from gdt.core.coords.spacecraft import SpacecraftFrame
from gdt.core.coords import SpacecraftFrame, Quaternion
from gdt.core.coords import *

from .frame import IntegralFrame
from .headers import SPIOrbitHeader

__all__ = ['IntegralOrbit']


class IntegralOrbit( SpacecraftFrameModelMixin, SpacecraftStatesModelMixin, FitsFileContextManager):  
    """Class for reading a INTEGRAL ORBIT file.
    """
    def __init__(self):
        super().__init__()

    @property
    def date(self):
        """(str): The Creation or modification date """
        return self._headers[1]['DATE']

    @property
    def ertfirst(self):
        """(str): Earth received time of the first packet"""
        return self._headers[1]['ERTFIRST']
    
    @property
    def ertlast(self):
        """(str): Earth received time of the last packet"""
        return self._headers[1]['ERTLAST']

    @property
    def revol_header(self):
        """(str): Revolution number"""
        return self._headers[1]['REVOL']
    
    @property
    def swid(self):
        """(integer): Science Window identifier"""
        return self._headers[1]['SWID']
    
    @property
    def sw_type(self):
        """(integer): Type of the Science Window"""
        return self._headers[1]['SW_TYPE']
    
    @property
    def swbound(self):
        """(integer): Reason for Science Window ending """
        return self._headers[1]['SWBOUND']
    
    @property
    def bcppid(self):
        """(integer): Broadcast packet pointing ID at ScW start """
        return self._headers[1]['BCPPID']

    @property
    def preswid(self):
        """(integer): Identifier of the previous Science Window """
        return self._headers[1]['PREVSWID']
    
    @property
    def obtstart(self):
        """(integer): OBT of the start of the Science Window """
        return self._headers[1]['OBTSTART']
    
    @property
    def obtend(self):
        """(integer): OBT of the end of the Science Window  """
        return self._headers[1]['OBTEND']

    @property
    def obtime(self):
        """(float): The Central on-board time """
        return self._obtime

    @property
    def revol(self):
        """(float): The Revolution Number"""
        return self._revol

    @property
    def revol_phase(self):
        """(float): The Phase of the revolution """
        return self._revol_phase

    @property
    def revol_frac(self):
        """(float): The Fractional revolution number """
        return self._revol_frac

    @property
    def distance(self):
        """(float): The Spacecraft distance from the Earth centre """
        return self._distance

    @property
    def xpos(self):
        """(float): The X component of the s/c position vector """
        return self._xpos

    @property
    def ypos(self):
        """(float): The Y component of the s/c position vector """
        return self._ypos

    @property
    def zpos(self):
        """(float): The Z component of the s/c position vector """
        return self._zpos

    @property
    def xvel(self):
        """(float): The X component of the s/c velocity vector """
        return self._xvel

    @property
    def yvel(self):
        """(float): The Y component of the s/c velocity vector """
        return self._yvel

    @property
    def zvel(self):
        """(float): The Z component of the s/c velocity vector """
        return self._zvel

    @property
    def ra_scx(self):
        """(float): Right ascension of s/c viewing direction """
        return self._ra_scx

    @property
    def dec_scx(self):
        """(float): Declination of s/c viewing direction """
        return self._dec_scx

    @property
    def ra_scz(self):
        """(float): Right ascension of the s/c Z-axis """
        return self._ra_scz

    @property
    def dec_scz(self):
        """(float): Declination of the s/c Z-axis """
        return self._dec_scz

    
    @property
    def posangle(self):
        """(float): Position angle in degrees """
        return self._posangle
    
    def get_spacecraft_frame(self) -> SpacecraftFrame:
        x_pointing = SkyCoord(self._ra_scx, self._dec_scx, unit='deg')
        z_pointing = SkyCoord(self._ra_scz, self._dec_scz, unit='deg')
        axes = SpacecraftAxes(x_pointing=x_pointing, z_pointing=z_pointing)
        x_pv = axes.pointing_vector('x')
        z_pv = axes.pointing_vector('z')
        if x_pv.ndim == 1:
            x_pv = x_pv.reshape(3, 1)
            z_pv = z_pv.reshape(3, 1)
        
        q1 = Quaternion.from_vectors(axes.x_vector[np.newaxis,:], x_pv.T).unit
        q1_arr = np.array([q1.x, q1.y, q1.z, q1.w])
            
        # apply X-axis rotation to equatorial frame Z axis
        z_vector = Rotation.from_quat(q1_arr.T).apply(axes.z_vector)

        # rotation between equatorial frame Z axis and INTEGRAL Z pointing
        q2 = Quaternion.from_vectors(z_vector, z_pv.T)
            
        quaternion = (q2 * q1).unit
        
        sc_frame = IntegralFrame(
            obsgeoloc=r.CartesianRepresentation(x=self._xpos,
                                                y=self._ypos,
                                                z=self._zpos, unit=u.km),
            obsgeovel=r.CartesianRepresentation(
                x=self._xvel * u.km / u.s,
                y=self._yvel * u.km / u.s,
                z=self._zvel * u.km / u.s,
                unit=u.km / u.s
            ),
            quaternion=quaternion
        )
        return sc_frame
    
    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a INTEGRAL Orbithist FITS file.
        
        Args:
            file_path (str): The file path of the FITS file
        
        Returns:        
            (:class:`IntegralOrbitHist`)
        """
        obj = super().open(file_path, **kwargs)
        hdrs = [hdu.header for hdu in obj.hdulist]
        obj._headers = SPIOrbitHeader.from_headers(hdrs)
        obj._date = obj._headers[1]['DATE']


        # store the data            
        obj._data = obj.hdulist[1].data
        obj._obtime = obj._data['OB_TIME']
        obj._revol = obj._data['REVOL']
        obj._revol_phase = obj._data['REVOL_PHASE']
        obj._revol_frac = obj._data['REVOL_FRAC']
        obj._distance = obj._data['DISTANCE']
        obj._xpos = obj._data['XPOS']
        obj._ypos = obj._data['YPOS']
        obj._zpos = obj._data['ZPOS']
        obj._xvel = obj._data['XVEL']
        obj._yvel = obj._data['YVEL']
        obj._zvel = obj._data['ZVEL']
        obj._ra_scx = obj._data['RA_SCX']
        obj._dec_scx = obj._data['DEC_SCX']
        obj._ra_scz = obj._data['RA_SCZ']
        obj._dec_scz = obj._data['DEC_SCZ']
        obj._posangle = obj._data['POSANGLE']

        return obj

