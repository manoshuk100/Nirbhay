import time
from raritan import rpc
from raritan.rpc import pdumodel


__author__ = 'Manoj Kumar Shukla-manoshuk@cisco.com'
__version__ = "1.0"

#######################################################
# Author: Manoj Kumar Shukla, Cisco Systems           #
# Date: 13th Jan, 2023                                #
#######################################################

###############################################################################
#                                                                             #
# This script will poweroff, poweron or toggle the outlets of RARITRAN PDUs   #
#                                                                             #
#                                                                             #
###############################################################################


def power_off(list):
    for l in list:
        agent = rpc.Agent("https", l, "apc1", "nbv12345")
        pdu = pdumodel.Pdu("/model/pdu/0", agent)
        # metadata = pdu.getMetaData()
        # print(metadata)
        outlets = pdu.getOutlets()
        for outlet in outlets:
            print(outlet.getMetaData())
            # outlets[0].setPowerState(pdumodel.Outlet.PowerState.PS_OFF)


def power_on(list):
    for l in list:
        agent = rpc.Agent("https", l, "apc1", "nbv12345")
        pdu = pdumodel.Pdu("/model/pdu/0", agent)
        # metadata = pdu.getMetaData()
        # print(metadata)
        outlets = pdu.getOutlets()
        for outlet in outlets:
            print(outlet.getMetaData())
            # outlets[0].setPowerState(pdumodel.Outlet.PowerState.PS_ON)



def toggle_power(list):
    for l in list:
        agent = rpc.Agent("https", l, "apc1", "nbv12345")
        pdu = pdumodel.Pdu("/model/pdu/0", agent)
        # metadata = pdu.getMetaData()
        # print(metadata)
        outlets = pdu.getOutlets()
        for outlet in outlets:
            print(outlet.getMetaData())
            # outlets[0].setPowerState(pdumodel.Outlet.PowerState.PS_OFF)
            time.sleep(2)
            # outlets[0].setPowerState(pdumodel.Outlet.PowerState.PS_ON)


def defer_power_off(list):
    print('You chose to defer power for 5 days')


if __name__ == '__main__':
    IP_LIST = ["10.127.49.67"]
    Dict = {1: power_off,
            2: power_on,
            3: toggle_power,
            4: defer_power_off
            }
    print('-' * 16 + 'WELCOME TO SMART PDU MGMT SYSTEM' + '-' * 16)
    print('Please choose from the below Options: \n1. Perform operation for all the PDUs \n2. Perform operation '
          'for selected few')
    choice = int(input('Option:'))
    if choice == 1:
        print("You choose to perform operation on all PDU'S")
        print(
            'What operation you want to perform: \n1. Poweroff all the PDUs\n2. Poweron all the PDUs\n3. Toggle Power for all the PDUs\n4. Defer power_off for all PDUs for 5days\n')
        option = int(input('Option:'))
        Dict[option](IP_LIST) if option in range(1, 5) else print('Entered option is not a valid option')
    elif choice == 2:
        print('You choose to perform operation on few PDUs.\nPlease enter the ip address(es) of the PDU(s)')
        IP = input("Comma Separated IP's:")
        IP_LIST = IP.split(',')
        print(IP_LIST)
        print(
            'What operation you want to perform: \n1. Poweroff all the PDUs\n2. Poweron all the PDUs\n3. Toggle '
            'Power for all the PDUs\n4. Defer power_off for all PDUs for 5days\n')
        option = int(input('Option:'))
        Dict[option](IP_LIST) if option in range(1, 5) else print('Entered option is not a valid option')
