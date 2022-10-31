#!/usr/bin/env python3
import main
import datetime
import subprocess
import os
import database_ops as db
import speedtest as sp


def get_and_save_devices():
	# Start on home directory
	subprocess.call("cd /home", shell=True)
	# It gets current date and time
	fecha_log = get_date()
	# Message to show on command line that it going to start look for devices
	print(" Start looking for devices connected to the network...")
	# It executes Wiom app to find the devices that are connected to the network and save all of them into
	# a log file
	subprocess.call("sudo wiom -w > ../Logs/logs_devices/last.log", shell=True)
	
	archivo = open("../Logs/logs_devices/last.log","r")
	
	# Call procesar_datos in order to obtain Ip, Mac, Name
	listaIp, listaMac, listaName  = process_data(archivo)
	
	# connect to ddbb
	connection = db.devices_database(listaIp, listaMac, listaName)
	
	# We rename the last log with todays date
	src = "../Logs/logs_devices/last.log"
	dst = "../Logs/logs_devices/%s.log" % fecha_log
	os.rename(src,dst)
	
def get_and_save_speeds():
    speed = sp.Speedtest()
    
    # We modify the round the results in order to see it better
    downspeed = round((round(speed.download()) / 1048576), 2)
    upspeed = round((round(speed.upload()) / 1048576), 2)

    db.speed_database(upspeed, downspeed)

#-----------------------------------------------------------------------------------
def get_date():
	fecha_log = datetime.datetime.now().strftime("%d_%m_%Y_%H:%M")
	return fecha_log


# To obtain data from logs
def process_data(archivo):
    listIp = []
    listMac = []
    listName = []
    lineas = archivo.readlines() 
    for i in lineas:
     if ("IP Addres"in i):
        listIp.append(i[12:26])
     if ("Mac Address"in i):
        listMac.append(i[14:-1])
     if ("Device"in i):
        listName.append(i[8:-1])
        
    return listIp, listMac, listName
#---------------------------------------------------------------------------------
    

def main():
    get_and_save_devices()
    get_and_save_speeds()

if __name__ == "__main__":
    main()
