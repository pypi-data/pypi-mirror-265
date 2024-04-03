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
from gdt.core.data_primitives import TimeBins
from gdt.core.file import FitsFileContextManager
from ..headers import Spi_acsHeaders


__all__ = ['Spi_acs']

class Spi_acs(FitsFileContextManager):
    """ Class for Spi-ACS lightcurve.
    """
    def __init__(self):
        super().__init__()
        self._data = None
        self._time = None
        self._rates = None
        self._error = None
        self._timezero = None
   
    @property
    def timezero(self):
        """(float): The reference 'zero' in time bin 
        in terms of the MET
        """
        return self._headers[1]['TIMEZERO']

    @property
    def obsdate(self):
        """(float): The observation date"""
        return self._headers[1]['DATE-OBS']

    @property
    def obsdateend(self):
        """(float): The observation date end"""
        return self._headers[1]['DATE-END']

    @property
    def tstart(self):
        """(float): The observation date"""
        return self._headers[1]['TSTART']

    @property
    def tstop(self):
        """(float): The observation date"""
        return self._headers[1]['TSTOP']

    @property
    def mjdref(self):
        """(float): The start of the lightcurve Time bins"""
        return self._headers[1]['MJDREF']

    @property
    def rates(self):
        """(float): The Rates """
        return self._rates

    @property
    def rates_error(self):
        """(float): The Rate Error"""
        return self._error

    @property
    def time(self):
        """(float): The start of the lightcurve Time bins"""
        return self._time

    
    @classmethod
    def open(cls, file_path, **kwargs):
        """Open and read a spi_acs file
        
        Args:
            file_path (str):  The file path of the spi_acs lightcurve file
        
        Returns:
            (:class:`~.spi_acs`)
        """
        obj = super().open(file_path, **kwargs)

        # get the headers
        hdrs = [hdu.header for hdu in obj.hdulist]
        obj._headers = Spi_acsHeaders.from_headers(hdrs)
        

        # store the data            
        obj._data = obj.hdulist['RATE'].data
        obj._rates = obj._data['RATE']
        obj._error = obj._data['ERROR']
        obj._time = obj._data['TIME']
        
        return obj
    
    
    def to_lightcurve(self):
        """Create the TimeBins object to plot the lightcurve 
            
        Returns:        
            (:class:`~.data_primitives.TimeBins`)
        """
        
        x= self._time
        x1=x[1:] + self.timezero
        x2=x[:-1] + self.timezero


        y=self._rates
        
        y1=y[1:]
        exp = x1-x2
        data = TimeBins(y1,x2,x1,exp)
        return data
