import sys
import serial
import time
import crc8
import RPi.GPIO as GPIO
from hx711 import HX711
import xlwt as xw
import datetime as dt

ser=serial.Serial(
    port = '/dev/ttyS0',
    baudrate = 115200,
    )
wb = xw.Workbook()
date_time= dt.datetime.now()
name=((str(date_time))[0:19])+('.xls')
name=name.replace(':', '-')
#workbook = xlsxwriter.Workbook(name)
xlsheet = wb.add_sheet('Test')
xlsheet.write(0, 0, 'RPM')
xlsheet.write(0, 1, 'Current')
xlsheet.write(0, 2, 'Thrust')
xlsheet.write(0, 3, 'Torque')

def check():
    while True:
        data=ser.read(10)
        hash = crc8.crc8()
        hash.update(data)
        key=hash.hexdigest() 
        if key=='00' :
            return
        else :
            ser.read(1)


torque_loadcell = HX711(27, 22) #3kg
thrust_loadcell = HX711(24 ,23) #10kg

torque_loadcell.set_reading_format("MSB", "MSB")
thrust_loadcell.set_reading_format("MSB", "MSB")

torque_loadcell.set_reference_unit(661.28)
thrust_loadcell.set_reference_unit(223.8)

torque_loadcell.reset()
thrust_loadcell.reset()

torque_loadcell.tare()
thrust_loadcell.tare()
row=1
while True :
    #current_hexa=bytes(0)
    #erpm_hexa=bytes(0)
    temp= b''
    lt=b''
    check()
    for i in range(0,10):
        temp=ser.read()
        #print(temp)
        lst=[lt,temp]
        
        if i==4 :
            current_hexa=b''.join(lst)
        elif i==8:
            #print(lt, temp)
            erpm_hexa=b''.join(lst)
        lt=temp
        
    current_int = int(current_hexa.hex(), 16)
    current = current_int/100
    erpm_int = int(erpm_hexa.hex(), 16)
    rpm=erpm_int*100/12
    thrust = thrust_loadcell.get_weight(1)
    torque = torque_loadcell.get_weight(1)
    xlsheet.write(row, 0, rpm)
    xlsheet.write(row, 1, current)
    xlsheet.write(row, 2, thrust)
    xlsheet.write(row, 3, torque)
    wb.save(name)
    print(f'Thrust= {thrust} \tTorque = {torque} \nCurrent = {current} \tRpm = {rpm}')
    row+=1
    
