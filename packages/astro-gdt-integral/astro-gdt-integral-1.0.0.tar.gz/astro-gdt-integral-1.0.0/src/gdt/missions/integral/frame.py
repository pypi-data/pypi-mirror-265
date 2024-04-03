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

import numpy as np
import astropy.units as u
import astropy.coordinates as a_coords
import astropy.coordinates.representation as r
from scipy.spatial.transform import Rotation
from astropy.coordinates import FunctionTransform, ICRS, frame_transform_graph
from gdt.core.coords.spacecraft import SpacecraftFrame
from gdt.core.coords.spacecraft.frame import spacecraft_to_icrs

__all__ = ['IntegralFrame', 'integral_to_icrs', 'icrs_to_integral']

class IntegralFrame(SpacecraftFrame):
    """
    The INTEGRAL spacecraft frame in azimuth and elevation.
    
    The frame is defined by orientation of the INTEGRAL X and Z axes in the J2000
    frame.  The axis directions are used to convert to a quaternion, which is
    used by SpacecraftFrame to do the frame transforms.

    """
    
    pass


@frame_transform_graph.transform(FunctionTransform, IntegralFrame, ICRS)
def integral_to_icrs(integral_frame, icrs_frame):
    """Convert from the INTEGRAL frame to the ICRS frame.
    
    Args:
        integral_frame (:class:`IntegralFrame`): The INTEGRAL frame
        icrs_frame (:class:`astropy.coordinates.ICRS`)
    
    Returns:
        (:class:`astropy.coordinates.ICRS`)
    """
    return spacecraft_to_icrs(integral_frame, icrs_frame)


@a_coords.frame_transform_graph.transform(a_coords.FunctionTransform, a_coords.ICRS, SpacecraftFrame)
def icrs_to_spacecraft_mod(icrs_frame, sc_frame):
    """
    Modified child class of 'icrs_to_spacecraft' to remove 'Nan' vale of 'el'.
    
    """
    xyz = icrs_frame.cartesian.xyz.value
    rot = Rotation.from_quat(sc_frame.quaternion)
    xyz_prime = rot.inv().apply(xyz.T)
    if xyz_prime.ndim == 1:
        xyz_prime = xyz_prime.reshape(1, -1)
    az = np.arctan2(xyz_prime[:, 1], xyz_prime[:, 0])
    mask = (az < 0.0)
    az[mask] += 2.0 * np.pi
    el = np.pi / 2.0 - np.arccos(np.clip(xyz_prime[:, 2],-1,1))
    return type(sc_frame)(az=az * u.radian, el=el * u.radian,
                            quaternion=sc_frame.quaternion)

@frame_transform_graph.transform(FunctionTransform, ICRS, IntegralFrame)
def icrs_to_integral(icrs_frame, integral_frame):
    """Convert from the ICRS frame to the INTEGRAL frame.
    
    Args:
        icrs_frame (:class:`astropy.coordinates.ICRS`)
        integral_frame (:class:`IntegralFrame`): The INTEGRAL frame
    
    Returns:
        (:class:`IntegralFrame`)
    """
    return icrs_to_spacecraft_mod(icrs_frame, integral_frame)


