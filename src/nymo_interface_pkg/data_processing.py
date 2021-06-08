import re
import datetime
from . import models

def create_log_from_log_line(log_line):
    original_list = log_line.split(", ")
    processed_list = [re.sub("^[^:\r\n]+:", '', i) for i in original_list]

    log = models.ShipLog()
    log.timestamp = datetime.datetime.strptime(processed_list[0], '%Y-%m-%d %H:%M:%S.%f')
    log.latitude = processed_list[1]
    log.longitude = processed_list[2]
    log.speed = processed_list[3]
    log.course = processed_list[4]
    log.ap_mode = processed_list[5]
    log.wind_direction = processed_list[6]
    log.wind_speed = processed_list[7]
    log.motor_left_power = processed_list[8]
    log.motor_right_power = processed_list[9]
    log.motor_left_current = processed_list[10]
    log.motor_right_current = processed_list[11]
    log.motor_left_rpm = processed_list[12]
    log.motor_right_rpm = processed_list[13]
    log.motor_left_temp = processed_list[14]
    log.motor_right_temp = processed_list[15]
    log.battery_current = processed_list[16]
    log.battery_voltage = processed_list[17]
    log.battery_soc = processed_list[18]
    log.front_left_sensor_dist = processed_list[19]
    log.front_center_sensor_dist = processed_list[20]
    log.front_right_sensor_dist = processed_list[21]
    log.ais_message = processed_list[22]

    return log 
