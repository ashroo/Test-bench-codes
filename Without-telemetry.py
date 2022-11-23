import sys
import serial
import time
import crc8
import RPi.GPIO as GPIO
from hx711 import HX711
import xlwt as xw
import datetime as dt
import os

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
xlsheet.write(0, 1, 'Thrust')
xlsheet.write(0, 2, 'Torque')


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
    thrust = thrust_loadcell.get_weight(1)
    torque = torque_loadcell.get_weight(1)
    xlsheet.write(row, 1, thrust)
    xlsheet.write(row, 2, torque)
    wb.save(os.path.join('Output', name))
    print(f'Thrust= {thrust} \tTorque = {torque}')
    row+=1
    
