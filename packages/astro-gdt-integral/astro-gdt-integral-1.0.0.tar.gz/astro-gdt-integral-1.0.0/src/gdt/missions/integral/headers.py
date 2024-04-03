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
from astropy.time import Time

from gdt.core.headers import Header, FileHeaders
from .time import *


__all__ = ['Spi_acsHeaders', 'SPIOrbitHeader' ]
# mission definitions
_telescope = 'INTEGRAL'
_instrument = 'SPI '
_timesys = 'TT'
_timeref = 'LOCAL'
_timeunit = 's'
_mjdref  = 51544.0


class SpiHeader(Header):
    pass

    
    def __setitem__(self, key, val):
        if not isinstance(key, tuple):
            if key.upper() == 'TSTART':
                self['DATE-OBS'] = Time(val, format='integral').iso 
            elif key.upper() == 'TSTOP':
                self['DATE-END'] = Time(val, format='integral').iso
            else:
                pass

            if 'INFILE' in key.upper():
                super(Header, self).__setitem__(key, val)
                return

        super().__setitem__(key, val)
    

# common keyword cards
_date_card = ('DATE', '', 'file creation or modification date (YYYY-MM-DDThh:mm:ss UT)')
_date_end_card = ('DATE-END', '', 'Date of end of observation')
_date_obs_card = ('DATE-OBS', '', 'Date of start of observation')
_ertfirst_card = ('ERTFIRST','', 'Earth received time of the first packet')       
_ertlast_card = ('ERTLAST','', 'Earth received time of the last packet')        
_revol_card = ('REVOL','', 'Revolution number')                              
_swid_card = ('SWID','', 'Science Window identifier')                      
_sw_type_card = ('SW_TYPE','',' Type of the Science Window')                     
_swbound_card = ('SWBOUND', '','Reason for Science Window ending')              
_bcppid_card = ('BCPPID', '', 'Broadcast packet pointing ID at ScW start')      
_PREVSWI_card = ('PREVSWID','', 'Identifier of the previous Science Window')     
_OBTSTART_card = ('OBTSTART', '', 'OBT of the start of the Science Window')       
_OBTEND_card = ('OBTEND', '', 'OBT of the end of the Science Window')  
_extname_card = ('EXTNAME', '', 'name of this binary table extension')
_extrel_card = ('EXTREL','', 'ISDC release number')
_instrument_card = ('INSTRUME', _instrument, 'Specific instrument used for observation')
_mjdref_card = ('MJDREF', _mjdref, 'MJD of the timezero')
_telescope_card = ('TELESCOP', _telescope, 'Name of mission/satellite')
_timeref_card = ('TIMEREF', _timeref, 'reference time')
_timesys_card = ('TIMESYS', _timesys, 'Time system used in time keywords') 
_timeunit_card = ('TIMEUNIT', _timeunit, 'Time since MJDREF, used in TSTART and TSTOP')
_tstart_card = ('TSTART', 0.0, '[INTEGRAL MET] Observation start time')
_tstop_card = ('TSTOP', 0.0, '[INTEGRAL MET] Observation stop time')
_timezero_card = ('TIMEZERO', 0.0, 'Trigger time relative to MJDREF, double precision')


class Spi_acsPrimaryHeader(SpiHeader):
    name = 'PRIMARY'

class Spi_acsSecondaryHeader(Spi_acsPrimaryHeader):
    name = 'RATE'
    keywords = [ _extname_card, _timesys_card, _instrument_card,
                _timeref_card, _tstart_card, _tstop_card,
                 _date_obs_card, _date_end_card, _mjdref_card, _telescope_card,
                  _timezero_card,  _timeunit_card, 
                ]


class Spi_acsHeaders(FileHeaders):
    """FITS headers for trigger TTE files"""
    _header_templates = [Spi_acsPrimaryHeader(), Spi_acsSecondaryHeader()]


class SPIOrbitPrimaryHeader(SpiHeader):
    name = 'PRIMARY'
    
class SPIOrbitDataHeader(SPIOrbitPrimaryHeader):
    name = 'INTL-ORBI-SCP'
    keywords = [_extname_card, _extrel_card, _telescope_card, _instrument_card, 
                  _date_card, _ertfirst_card, _ertlast_card, _revol_card, _swid_card,
                _sw_type_card, _swbound_card, _bcppid_card, _PREVSWI_card, _OBTSTART_card, 
                _OBTEND_card]


class SPIOrbitHeader(FileHeaders):
    """FITS headers for trigger TTE files"""
    _header_templates = [SPIOrbitPrimaryHeader(), SPIOrbitDataHeader()]
