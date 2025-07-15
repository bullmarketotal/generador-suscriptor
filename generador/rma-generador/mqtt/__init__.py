from enum import IntEnum, auto

class TipoMensaje(IntEnum):
    STATUS = 0
    TEMP_T = 1  # Temperature
    TEMP2_T = 2  # Temperature #2
    HUMIDITY_T = 3  # Relative Humidity
    PRESSURE_T = 4  # Atmospheric Pressure
    LIGHT_T = 5  # Light (lux)
    SOIL_T = 6  # Soil Moisture
    SOIL2_T = 7  # Soil Moisture #2
    SOILR_T = 8  # Soil Resistance
    SOILR2_T = 9  # Soil Resistance #2
    OXYGEN_T = 10  # Oxygen
    CO2_T = 11  # Carbon Dioxide
    WINDSPD_T = 12  # Wind Speed
    WINDHDG_T = 13  # Wind Direction
    RAINFALL_T = 14  # Rainfall
    MOTION_T = 15  # Motion
    VOLTAGE_T = 16  # Voltage
    VOLTAGE2_T = 17  # Voltage #2
    CURRENT_T = 18  # Current
    CURRENT2_T = 19  # Current #2
    IT_T = 20  # Iterations
    LATITUDE_T = 21  # GPS Latitude
    LONGITUDE_T = 22  # GPS Longitude
    ALTITUDE_T = 23  # GPS Altitude
    HDOP_T = 24  # GPS HDOP
    LEVEL_T = 25 # Fluid Level
