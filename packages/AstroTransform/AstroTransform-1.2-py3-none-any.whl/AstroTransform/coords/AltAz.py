""" 
convert target to alt az
"""

import numpy as np
from datetime import datetime, timedelta
from AstroTransform.time import JD, lst
from AstroTransform.coords import hour_angle
from astropy.time import Time

def to_alt_az(RA, DEC, Lat, Lon, obs_time, time_zone=0):
    """
    Convert a target's RA and DEC to Altitude and Azimuth.
    
    Parameters
    ----------
    RA : float
        The right ascension of the target in hours.
    DEC : float
        The declination of the target in degrees.
    Lat : float
        The latitude of the observer in degrees.
    Lon : float
        The longitude of the observer in degrees.
    obs_time : datetime.datetime
        The local time of the observation
    
    Returns
    -------
    float
        The altitude of the target in degrees.
    float
        The azimuth of the target in degrees.
        
    """
    if isinstance(obs_time, Time):
        obs_time = obs_time.to_datetime()
    if not isinstance(RA, (int, float)):
        raise TypeError("Expected a float or int for 'RA'.")
    if not isinstance(DEC, (int, float)):
        raise TypeError("Expected a float or int for 'DEC'.")
    if not isinstance(Lat, (int, float)):
        raise TypeError("Expected a float or int for 'Lat'.")
    if not isinstance(Lon, (int, float)):
        raise TypeError("Expected a float or int for 'Lon'.")
    if not isinstance(obs_time, datetime):
        raise TypeError("Expected a datetime.datetime object for 'obs_time'.")

    #convert to radians
    RA_rad = np.deg2rad(RA * 15.0)
    DEC_rad = np.deg2rad(DEC)
    Lat_rad = np.deg2rad(Lat)
    Lon_rad = np.deg2rad(Lon)

    #calculate LST
    LST = lst.lst(obs_time, Lon, time_zone)
    
    #calculate hour angle
    HA = hour_angle.hourangle(LST, RA)
    HA_rad = np.deg2rad(HA*15.0)
    LSTrad = np.deg2rad(LST*15.0)
    # calculate altitude
    sin_alt = np.sin(DEC_rad)*np.sin(Lat_rad) + np.cos(DEC_rad)*np.cos(Lat_rad)*np.cos(HA_rad)
    alt = np.arcsin(sin_alt)
    #calculate azimuth #
    tolerance = 1e-6
    cos_az = (np.sin(DEC_rad) - np.sin(alt)*np.sin(Lat_rad))/(np.cos(alt)*np.cos(Lat_rad))
    if not -1 - tolerance <= cos_az <= 1 + tolerance:
        # Log a warning or raise an error
        print(f"Warning: cos_az value {cos_az} is significantly out of range.")
    cos_az = np.clip(cos_az, -1.0, 1.0)
    az = np.arccos(cos_az)

    if np.sin(HA_rad) > 0:
        az = 2*np.pi - az
    else:
        az = az
    #convert to degrees
    alt = np.rad2deg(alt)
    az = np.rad2deg(az)


    return alt, az

def max_alt(DEC, Lat):
    """
    Calculate the maximum altitude of a target.
    
    Parameters
    ----------
    DEC : float
        The declination of the target in degrees.
    Lat : float
        The latitude of the observer in degrees.    
    Returns
    -------
    float
        The maximum altitude of the target in degrees.
        
    """
    if not isinstance(DEC, (int, float)):
        raise TypeError("Expected a float or int for 'DEC'.")
    if not isinstance(Lat, (int, float)):
        raise TypeError("Expected a float or int for 'Lat'.")
    #convert to radians

    DEC_rad = np.deg2rad(DEC)
    Lat_rad = np.deg2rad(Lat)

    
    #calculate hour angle
    HA = 0 # hour angle 0 when target transits
    HA_rad = np.deg2rad(HA*15.0)

    # calculate altitude
    sin_alt = np.sin(DEC_rad)*np.sin(Lat_rad) + np.cos(DEC_rad)*np.cos(Lat_rad)*np.cos(HA_rad)
    alt = np.arcsin(sin_alt)
    #convert to degrees
    alt = np.rad2deg(alt)
    return alt

