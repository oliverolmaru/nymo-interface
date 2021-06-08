from sqlalchemy import create_engine
from .database import SessionLocal
import json
from . import models
import datetime
import requests
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.decl_api import registry
import time
from .dummy_generation import generate_dummy_data
import threading
from .data_processing import create_log_from_log_line 


def new_alchemy_encoder():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    fields[field] = obj.__getattribute__(field)
                    #let's work with datetime
                    if(isinstance(fields[field], datetime.datetime) or isinstance(fields[field], datetime.date)):
                        fields[field] = fields[field].isoformat()
                # a json-encodable dict
                return fields
            if isinstance(obj, registry):
                return None
            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder

def get_latest_log():
    db = SessionLocal()
    try:
        firstLog = db.query(models.ShipLog).order_by(models.ShipLog.timestamp.desc()).first()
        #print(firstLog.timestamp)
        return firstLog
    except (Exception) as error:
        print(error)
        #print("DB_FAILURE")
        return None
    finally:
        db.close()
    return None
            

def add_to_queue(log: models.ShipLog):
    db = SessionLocal()
    try:
        db.add(log)
        db.commit()
        #print("success")
        return 
    except (Exception) as error:
        print(error)
        #print("DB_FAILURE")
        return
    finally:
        db.close()

def add_log_string_to_queue(logStr: str):
    print("NYMO_INTERFACE: Adding log to queue")
    try:
        log = create_log_from_log_line(logStr)
    except (Exception) as error:
        print(error)
        print("PARSE_FAILURE")
        return

    db = SessionLocal()
    try:
        db.add(log)
        db.commit()
        #print("success")
        return 
    except (Exception) as error:
        print(error)
        #print("DB_FAILURE")
        return
    finally:
        db.close()        

def remove_log_from_db(log: models.ShipLog):
    db = SessionLocal()
    try:
        db.delete(log)
        db.commit()
        return 
    except (Exception) as error:
        print(error)
        return
    finally:
        db.close()
    
    return

#Create Databases
e = create_engine('sqlite:///database.db')
models.Base.metadata.create_all(bind=e)


# log = models.ShipLog()
# log.timestamp = datetime.datetime(2020, 7, 21,13,47,24)
# add_to_queue(log)

def upload_data_to_server():
    print("NYMO_INTERFACE: Starting COMMUNICATION THREAD")
    ACCESS_TOKEN = "Bearer 1cd90fde1fde4047b7bd5675869dfcb1"
    db = SessionLocal()
    try:
        while(1):
            time.sleep(0.05)
            log = get_latest_log()
            #No logs to upload
            if(log == None):
                #print("no logs")
                continue
            try:
                url = 'https://nymo-server.appspot.com/ships/log'
                headers = {"Authorization": ACCESS_TOKEN}
                data = json.dumps(log, cls=new_alchemy_encoder(), check_circular=False)
                x = requests.post(url, data = data, headers=headers)
                print("DATA UPLOADED")
                remove_log_from_db(log)
            except (Exception) as error:
                print(error)
                print("DB_FAILURE")
                return
    except (Exception) as error:
        print(error)
        print("GLOBAL ERROR")
        return
    finally:
        db.close()


        
        


def simulate_ship(sleepBetweenLogs):
    while(1):
        #print(f'Generating data({datetime.datetime.now()}')
        log = generate_dummy_data()
        add_to_queue(log)
        time.sleep(sleepBetweenLogs)

def main():
    print("Starting SIMULATION thread")
    x1 = threading.Thread(target=simulate_ship, args=(0.5,))
    x1.daemon = True
    x1.start()
    print("Starting COMMUNICATION thread")
    x2 = threading.Thread(target=upload_data_to_server)
    x2.daemon = True
    x2.start()
    while(1):
        time.sleep(1)
    # print("Sending request!")
    # ACCESS_TOKEN = "Bearer e3ce27ae63054c1896abca88713c8e87"
    # log = get_latest_log()
    # #print(log.to_dict())
    # if(log == None):
    #     return

    # url = 'http://127.0.0.1:8000/ships/log'
    # headers = {"Authorization": ACCESS_TOKEN}
    # data = json.dumps(log, cls=new_alchemy_encoder(), check_circular=False)
    # x = requests.post(url, data = data, headers=headers)
    

    # print(x.content)


if __name__ == "__main__":
    main()
#add_log_string_to_queue("date and time:2020-07-21 11:36:14.103923, lat:59.60728, lon:25.928736666666666, Speed:0.4, Course:95.4, AP_mode:ACRO, Wind_direction:242, Wind_speed:4.9, M1_power:0, M2_power:0, M1_current:0.0, M2_current:-0.1, M1_rpm:0.0, M2_rpm:0.0, M1_temp:-1, M2_temp:32767, Battery_current:-0.02, Battery_voltage:65.535, Battery_SOC:6553.5, Left_front_US_dist:1130, Middle_front_US_dist:1124, Right_front_US_dist:1122, AIS_msg:$GPRMC,083613.00,A,5936.43675,N,02555.72445,E,0.495,97.60,210720,,,D*5F")


