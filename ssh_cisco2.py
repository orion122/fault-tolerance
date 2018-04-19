import crassh
import socket
from time import sleep

port = 22
main_cisco = '192.168.117.141'
primary = '195.133.196.173'
username = 'admin'
password = 'QwertY651397'


def switch_main_cisco_to_primary():
    hostname = crassh.connect(main_cisco, username, password)
    crassh.send_command("conf t", hostname)
    output = crassh.send_command("hostname CSR-TEST1-Primary", hostname, 5)
    crassh.disconnect()
    #print(output)


def switch_main_cisco_to_secondary():
    hostname = crassh.connect(main_cisco, username, password)
    crassh.send_command("conf t", hostname)
    output = crassh.send_command("hostname CSR-TEST1-Secondary", hostname, 5)
    crassh.disconnect()
    #print(output)


def was_available():
    with open('was_available.txt', 'r') as file:
        return str_to_bool(file.read())


def write_last_availability(state):
    with open('was_available.txt', 'w') as file:
        file.write(str(state))


def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False


def is_available():
    s = socket.socket()
    try:
        s.connect((primary, port))
        s.settimeout(3)
        print('Available')
        return True
    except:
        print('Not Available')
        return False
    finally:
        s.close()


def switch():
    isAvailable = is_available()
    wasAvailable = was_available()

    if isAvailable and not wasAvailable:
        write_last_availability(isAvailable)
        switch_main_cisco_to_primary()
    elif not isAvailable and wasAvailable:
        write_last_availability(isAvailable)
        switch_main_cisco_to_secondary()


while True:
    switch()
    sleep(3)
