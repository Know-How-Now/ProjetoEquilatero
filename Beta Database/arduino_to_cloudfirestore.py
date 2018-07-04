import serial
import csv
import time
import datetime
import keyboard
from tqdm import tqdm
import custom_dictionaries as c_dict
import custom_classes as c_class
import query_functions as query

# DEFINIR COLETA DE DADOS #
serial_port = serial.Serial('/dev/ttyUSB0', 38400)
incoming_data = serial_port.readline().decode('utf-8')
#data_decoded = incoming_data_bytes.decode("utf-8")

# FLAGS
flag_next = '\t'
flag_done = 'd'
flag_index = b'i'
get_smartband_data = b'b'
get_sensor_data = b's'
clear_eeprom = b'e'
configure_smartband = b'c'

# COLLECTED DATA ARRAYS
smartband_data = []
sensor_data = []

#SERIAL COMMUNICATION
print('Initializing serial communication...')
data_collected = 0
pbar = tqdm(total=100)   
while True:
    print("Communication established.\nPlease select one choice at a time:\n'b': collect smartband data\n's': collect sensor data\n'e': clear device's memory\n'c': configure smartband\n'd': done\n")
    key = keyboard.read_key()
    try:
        if keyboard.is_pressed(key):
            serial_port.writef(b'{}'.format(key))
            if key == 'b':
                smartband_data.append(incoming_data)
            if key == 's':
                sensor_data.append(incoming_data)
            if key == 'c':
                control_id,profile_id = (int (x) for x in input("Please enter a Smartband Control ID and User Profile ID (separated by comma):\n"))
                serial_port.write(control_id)
                serial_port.write(profile_id)
            if incoming_data == '\t':
                continue
            if incoming_data == 'd':
                print('Configuration settings and data collection done!')
                choice_database = input("Do you wish to send collected information to the database? (y/n):\n")
                if choice_database == 'n':
                    choice_csv = input("Save data in an 'csv' document? (y/n)\n")
                    if choice_csv == 'n':
                        print("Devices are cleared and ready for setup!\n Closing program...")
                        time.sleep(3)
                        exit(1)
                    else: ##IMPROVE THIS CSV FILE FORMATTING
                        csvfile_path = input("Please input the path for your CSV document:\n")
                        with open(csvfile_path, 'w', newline='') as csv_mode:
                            csv.writer(csv_mode).writerow(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                            smartband_row = csv.DictWriter(csv_mode, fieldnames=['Smartband Data'])
                            smartband_row.writeheader()
                            smartband_row.writerow({'Smartband Data': smartband_data})
                            sensor_row = csv.DictWriter(csv_mode, fieldnames=['Sensor Data'])
                            sensor_row.writeheader()
                            sensor_row.writerow({'Sensor Data': sensor_data})
        else: #edit 
            sensor_ref = query.db.collection('Sensors').document(id)
            sensor_ref.set(c_class.Timestamp(random_sensor_data()).to_dict())
            i = 1
            while i < 5:
                sensor_ref.update(c_class.Timestamp(random_sensor_data()).to_dict())
                pbar.update(+(1/4))
                i = i + 1
            data_created = data_created + 1
            arduino.write(b'b')
            print('Erasing wristband data...')
    except:
        continue
valid_data = (arduino_data[0:-2])
print('Parabens, voce percorreu {} metros na ultima trilha!'.format(valid_data[2]))
print(valid_data)
print('SensorID: {}, RegionID: {}, Sensor Position: {}, Avg. Attempt: {}, State: {}, Connections: {}'.format(
    valid_data[0],valid_data[1],valid_data[2],valid_data[3],valid_data[4],valid_data[5]))
bs.send_Sensor_DATA(u'sensores',u'Sx00011',valid_data)
print("\nSuccesfully sent all {} 'Sponsor' data samples to the Database!".format(sample_data_ammount))

def structure_incoming_data(smartband_array, sensor_array):
    profile_id = smartband_data[0]
    control_id = smartband_data[1]
    sensor_data_splitted = sensor_data.split('i')
    for sensor in sensor_data_splitted:
        return sensor
