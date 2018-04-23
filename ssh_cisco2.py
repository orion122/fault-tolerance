import crassh
import socket, os
from time import sleep
import config


def switch_main_cisco_to_primary():
    hostname = crassh.connect(config.main_cisco, config.username, config.password)
    crassh.send_command("conf t", hostname)
    output = crassh.send_command("hostname CSR-TEST1-Primary", hostname, 1)
    crassh.disconnect()
    #print(output)


def switch_main_cisco_to_secondary():
    hostname = crassh.connect(config.main_cisco, config.username, config.password)
    crassh.send_command("conf t", hostname)
    output = crassh.send_command("hostname CSR-TEST1-Secondary", hostname, 1)
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


def is_available_by_SSH():
    s = socket.socket()
    try:
        s.connect((config.primary, config.port))
        s.settimeout(1)
        print('Available By SSH')
        return True
    except:
        print('Not Available By SSH')
        return False
    finally:
        s.close()


def is_available_by_ICMP():
    exitStatus = os.system("ping -c 1 -W 1 " + config.primary)
    return print('True') if exitStatus == 0 else print('False')


def is_available_now(isAvailableBySSH, isAvailableByICMP):
    return isAvailableBySSH or isAvailableByICMP


def isStateChanged(isAvailableNow, isAvailableBefore):
    return isAvailableNow != isAvailableBefore


def switch():
    isAvailableNow = is_available_now(is_available_by_SSH(), is_available_by_ICMP())
    wasAvailableBefore = was_available_before()

    if isStateChanged(isAvailableNow, wasAvailableBefore):
        save_availability_state(isAvailableNow)
        switch_main_cisco_to_primary() if isAvailableNow else switch_main_cisco_to_secondary()

while True:
    switch()
    sleep(3)