import crassh
import socket
from time import sleep
import config


def switch_main_cisco_to_primary():
    hostname = crassh.connect(config.main_cisco, config.username, config.password)
    crassh.send_command("conf t", hostname)
    output = crassh.send_command("hostname CSR-TEST1-Primary", hostname, 3)
    crassh.disconnect()
    #print(output)


def switch_main_cisco_to_secondary():
    hostname = crassh.connect(config.main_cisco, config.username, config.password)
    crassh.send_command("conf t", hostname)
    output = crassh.send_command("hostname CSR-TEST1-Secondary", hostname, 3)
    crassh.disconnect()
    #print(output)


def was_available_before():
    with open('was_available.txt', 'r') as file:
        return str_to_bool(file.read())


def save_availability_state(state):
    with open('was_available.txt', 'w') as file:
        file.write(str(state))


def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False


def is_available_now():
    s = socket.socket()
    try:
        s.connect((config.primary, config.port))
        s.settimeout(3)
        print('Available')
        return True
    except:
        print('Not Available')
        return False
    finally:
        s.close()


def isStateChanged(isAvailableNow, isAvailableBefore):
    return isAvailableNow != isAvailableBefore


def switch():
    isAvailableNow = is_available_now()
    wasAvailableBefore = was_available_before()

    if isStateChanged(isAvailableNow, wasAvailableBefore):
        save_availability_state(isAvailableNow)
        if isAvailableNow:
            switch_main_cisco_to_primary()
        else:
            switch_main_cisco_to_secondary()

while True:
    switch()
    sleep(3)