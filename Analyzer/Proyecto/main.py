#!/usr/bin/env python3
import main
import datetime
import subprocess
import os
import database_ops as db

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
	listaIp, listaMac, listaName  = procesar_datos_ip(archivo)
	
	# connect to ddbb
	#connection = db.connect_database()
	
	
	
	# guardar_datos_dispositivos(ip,mac,nombre)
	src = "../Logs/logs_devices/last.log"
	dst = "../Logs/logs_devices/%s.log" % fecha_log
	os.rename(src,dst)
	
	

#-----------------------------------------------------------------------------------
def get_date():
	fecha_log = datetime.datetime.now().strftime("%d_%m_%Y_%H:%M")
	return fecha_log


# To obtain data from logs
def procesar_datos_ip(archivo):
    listIp = []
    listMac = []
    listName = []
    lineas = archivo.readlines() 
    for i in lineas:
     if ("IP Addres"in i):
        listIp.append(i[12:-1])
     if ("Mac Address"in i):
        listMac.append(i[14:-1])
     if ("Device"in i):
        listName.append(i[8:-1])
        
    return listIp, listMac, listName
#---------------------------------------------------------------------------------
    

def main():
    get_and_save_devices()
    #procesar_datos()

if __name__ == "__main__":
    main()
