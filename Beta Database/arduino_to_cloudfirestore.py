import serial
import csv
import time
import datetime
from tqdm import tqdm
import custom_dictionaries as c_dict
import custom_classes as c_class
import query_functions as query

# DEFINIR COLETA DE DADOS #
serial_port = serial.Serial('/dev/ttyUSB0',38400)
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
print(f"{flag_done}")
# COLLECTED DATA ARRAYS
smartband_data = []
sensor_data = []

#SERIAL COMMUNICATION
print('Initializing serial communication...')
data_collected = 0
pbar = tqdm(total=100)   
while True:
    config_mode = input("Communication established.\nPlease select one choice at a time:\n'b': collect smartband data\n's': collect sensor data\n'e': clear device's memory\n'c': configure smartband\n'd': done\n")
    if config_mode == 'b':
        serial_port.writef(b'{}')
        smartband_data.append(incoming_data)
    if config_mode == 's':
        serial_port.write(b's')
        sensor_data.append(incoming_data)
        if incoming_data == 'i':
            sensor_data.append('i')
    if config_mode == 'e':
        serial_port.write(b'e')
    if config_mode == 'c':
        serial_port.write(b'c')
        control_id,profile_id = (int (x) for x in input("Please enter a Smartband Control ID and User Profile ID (separated by comma):\n"))
        serial_port.write(control_id)
        serial_port.write(profile_id)
    if incoming_data == '\t':
        continue
    if incoming_data == 'd':
            print('Configuration settings and data collection done!')
            choice = input("Do you wish to send collected information to the database? (y/n):\n")
            if choice == 'n':
                choice = input("Save data in a .txt document? (y/n)\n")
                    if choice == 'n':
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
        if data_decoded == end_arduino:
            print('Artefato pronto para proxima trilha!')
            break
    else:
        continue
valid_data = (arduino_data[0:-2])
print('Parabens, voce percorreu {} metros na ultima trilha!'.format(valid_data[2]))
print(valid_data)
print('SensorID: {}, RegionID: {}, Sensor Position: {}, Avg. Attempt: {}, State: {}, Connections: {}'.format(
    valid_data[0],valid_data[1],valid_data[2],valid_data[3],valid_data[4],valid_data[5]))
bs.send_Sensor_DATA(u'sensores',u'Sx00011',valid_data)
print("\nSuccesfully sent all {} 'Sponsor' data samples to the Database!".format(sample_data_ammount))
