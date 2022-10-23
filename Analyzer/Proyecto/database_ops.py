#!/usr/bin/env python3
import mariadb
import sys


def connect_database():
    try:
        connection = mariadb.connect(
        user="user1",
        password="password",
       # host="192.168.0.122",
       # port=3306,
        database="proyeto")
        
    except mariadb.Error as e:
    
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
        
    return connection;
    

#def add_data(connection,Ip,Mac,Name):
    

#def db_exists():
    
    