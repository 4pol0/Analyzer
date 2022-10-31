#!/usr/bin/env python3
import mysql.connector as mariadb
import sys
import main as mai
from pathlib import Path


def devices_database(Ip, Mac, Name):
    
    # If the file does not exist, if not it will be created
    file_registry = Path("../Logs/log_history_devices.log")
    file_registry.touch(exist_ok=True)
    fi_re = open(file_registry,'a')
    
    # We connect to database
    mariadb_connection = database_connection()
    cursor = mariadb_connection.cursor(buffered=True)
    
    # We delete all records from current_devices table
    query_delete = """TRUNCATE TABLE current_devices"""
    cursor.execute(query_delete)
    mariadb_connection.commit()
    #--------------------------------------------------
    
    date = mai.get_date();
    
    for (m,i,n) in zip(Mac,Ip,Name):
        _mac = m 
        _ip  = i 
        _name = n
        print(_mac)
        
       # Now we are going to check if in the devices that the script registred are new.
       # query_new = ()
        result = cursor.execute("SELECT * FROM devices_registry WHERE Mac='{_mac}'")
        
        if (result == None):
            fi_re.write(date + " - A new device was connect to the network with MAC " + _mac + ". The name is '"+ _name +"'\n")
        
        # We add devices to de registry
        query_1 = """INSERT INTO devices_registry(Mac, Ip, Name, Date) values (%s, %s, %s, %s)"""
        cursor.execute(query_1,(_mac, _ip, _name, date))
        # We add devices to current devices tables
        query_2 = """INSERT INTO current_devices(Mac, Ip, Name) values (%s, %s, %s)"""
        cursor.execute(query_2,(_mac, _ip, _name))
        mariadb_connection.commit()
        
    

    
def speed_database(up,down):
    
    mariadb_connection = database_connection()
    cursor = mariadb_connection.cursor(buffered=True)
    
    date = mai.get_date()
    
    # We add speeds to de registry
    query_1 = """INSERT INTO network_speed(Speed_up, Speed_down, Date) values (%s, %s, %s)"""
    cursor.execute(query_1,(up, down, date))
    mariadb_connection.commit()
    
def database_connection():
    
    try:
        mariadb_connection= mariadb.connect(user='root', password='root', host='localhost', port='3306', database='analyzer')
 
    except mariadb.Error as e:
    
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
        
    return mariadb_connection
    
    
    