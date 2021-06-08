from . import models
import datetime
import random

def generate_dummy_data(timestamp = None):
    log = models.ShipLog()

    if(timestamp == None):
        timestamp = datetime.datetime.now()
        
    log.timestamp = timestamp
    #Navigation
    log.latitude = 59.4775 + random.random()/100
    log.longitude = 24.775 + random.random()/100
    log.speed = 5 + random.random()*2
    log.course = 90 + random.random()*20
    log.ap_mode = "ACRO"
    log.wind_direction = 240 + random.random()*70
    log.wind_speed = 5 + random.random()*2
    log.ais_message = "$GPRMC,104720.00,A,5936.24062,N,02555.38227,E,0.012,,210720,,,D*70"
    log.front_left_sensor_dist = 1000 + random.random()*200
    log.front_center_sensor_dist = 1000 + random.random()*200
    log.front_right_sensor_dist = 1000 + random.random()*200
    #Propulsion
    log.motor_left_temp = 50 + random.random()*15
    log.motor_left_power = 1200 + random.random()*200
    log.motor_left_current = 1200 + random.random()*200
    log.motor_left_rpm = 3000 + random.random()*500
    log.motor_right_temp = 50 + random.random()*15
    log.motor_right_power = 1200 + random.random()*200
    log.motor_right_current = 1200 + random.random()*200
    log.motor_right_rpm = 3000 + random.random()*500
    #Power
    log.battery_current = 50 + random.random()*5
    log.battery_voltage = 11 + random.random()*1.5
    log.battery_soc = 3000 + random.random()*500

    return log