import serial
import time
import sys
sys.path.insert(0, '/Users/cbmelo/Documents/PycharmProjects/CESAR/Primerio_Periodo/Equilatero/Alpha/Database/alpha_db_V36.py')
import alpha_db_V36.py

# DEFINIR COLETA DE DADOS #
arduino = serial.Serial('/dev/ttyUSB0',38400)
arduino_data = []
start_arduino = 999999997
flag_arduino = 999999998
end_arduino = 999999999

while True:
    data_bytes = arduino.readline()
    if data_bytes:
        data_decoded = int(data_bytes.decode("utf-8"))
        arduino_data.append(data_decoded)
        if data_decoded == flag_arduino:
            print('Done decoding...')
            #programar pra enviar dados pro servidor#
            print('Sending data to server...')
            #programar para limpar EEPROM
            arduino.write(b'b')
            print('Erasing wristband data...')
        if data_decoded == end_arduino:
            print('Artefato pronto para proxima trilha!')
            break
        else:
            continue
time.sleep(1)
valid_data = (arduino_data[0:-2])
print('Parabens, voce percorreu {} metros na ultima trilha!'.format(valid_data[2]))
print(valid_data)
print('SensorID: {}, RegionID: {}, Sensor Position: {}, Avg. Attempt: {}, State: {}, Connections: {}'.format(
    valid_data[0],valid_data[1],valid_data[2],valid_data[3],valid_data[4],valid_data[5]))
bs.send_Sensor_DATA(u'sensores',u'Sx00011',valid_data)