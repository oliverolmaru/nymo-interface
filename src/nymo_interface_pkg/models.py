from sqlalchemy import Column, String, Integer, Float, DateTime  
from sqlalchemy.ext.declarative import declarative_base
from .database import Base


class ShipLog(Base):
    __tablename__ = 'ship_log'

    #General
    timestamp = Column(DateTime, primary_key=True)
    #Navigation
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    course = Column(Float)
    ap_mode = Column(String)
    wind_direction = Column(Float)
    wind_speed = Column(Float)
    ais_message = Column(String)
    front_left_sensor_dist = Column(Integer)
    front_center_sensor_dist = Column(Integer)
    front_right_sensor_dist = Column(Integer)
    #Propulsion
    motor_left_temp = Column(Integer)
    motor_left_power = Column(Integer)
    motor_left_current = Column(Float)
    motor_left_rpm = Column(Float)
    motor_right_temp = Column(Integer)
    motor_right_power = Column(Integer)
    motor_right_current = Column(Float)
    motor_right_rpm = Column(Float)
    #Power
    battery_current = Column(Float)
    battery_voltage = Column(Float)
    battery_soc = Column(Float)

class RawLog(Base):
    __tablename__ = 'ship_log_raw'

    #General
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True)
    #Navigation
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    course = Column(Float)
    ap_mode = Column(String)
    wind_direction = Column(Float)
    wind_speed = Column(Float)
    ais_message = Column(String)
    front_left_sensor_dist = Column(Integer)
    front_center_sensor_dist = Column(Integer)
    front_right_sensor_dist = Column(Integer)
    #Propulsion
    motor_left_temp = Column(Integer)
    motor_left_power = Column(Integer)
    motor_left_current = Column(Float)
    motor_left_rpm = Column(Float)
    motor_right_temp = Column(Integer)
    motor_right_power = Column(Integer)
    motor_right_current = Column(Float)
    motor_right_rpm = Column(Float)
    #Power
    battery_current = Column(Float)
    battery_voltage = Column(Float)
    battery_soc = Column(Float)