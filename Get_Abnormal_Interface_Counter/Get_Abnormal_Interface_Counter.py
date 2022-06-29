import re
import requests
from netmiko import ConnectHandler
import time
import logging

__author__ = 'Manoj Kumar Shukla-manoshuk@cisco.com'
__version__ = "1.0"

#######################################################
# Author: Manoj Kumar Shukla, Cisco Systems           #
# Date: 28th June, 2022                               #
#######################################################

###############################################################################
#                                                                             #
# This script will validate if any interface rate is more than usual and then #
# reports to the user via Cisco Webex teams.                                  #
#                                                                             #
###############################################################################


def find_rate(ip):
    device = ConnectHandler(device_type='cisco_nxos', ip=ip, username='<replace with username>', password='<replace with password>')
    count = 1
    FORMAT = "[%(asctime)s] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    while True:
        output_1 = device.send_command("show interface status up")
        output_2 = re.findall(r"Eth\d/\d{1,2}", output_1)
        print(output_2)
        print("*" * 30, f'Round {count} Started', "*" * 30)
        logging.info(f'Round {count} Started')
        for interface in output_2:
            try:
                cmd = "show interface" + " " + interface
                output_3 = device.send_command(cmd)
                output_4 = re.search(r'input\srate\s\d{1,9}\.\d{1,9}\sGbps', output_3)
                rate = (output_4.group().split())
                if float(rate[2]) > 10:
                    t = time.localtime()
                    print(f'A higher rate is recorded on {interface} of {(rate[2]+" "+rate[3])} at {time.asctime(t)}')
                    logging.info(f'Higher rate on {interface} detected,rate is {(rate[2] + " " + rate[3])}')
                    sendmsg('Higher rate of traffic is recorded on'+" "+interface+' with a rate of'+ " "+rate[2]+" "+rate[3]+' on'+ ' '+ time.asctime(t))
                else:
                    print(f'{interface} working within normal line rate,rate is {(rate[2]+" "+rate[3])}')
            except AttributeError:
                print(f'{interface} interface do not have counter in Gbps')
        count += 1


def sendmsg(str):
    auth_token = "<insert your bot secret token created from https://developer.webex.com/docs/bots>"
    message_url = "https://api.ciscospark.com/v1/messages"
    list = ["<insert Cisco id created>"]
    for item in list:
        message = {"toPersonEmail": item + '@cisco.com', "text": str}
        requests.post(message_url, headers={"Authorization": "Bearer %s" % auth_token}, json=message)


def main():
    ip = "<Enter the mgmt IP to ssh into teh device>"
    find_rate(ip)


if __name__ == '__main__':
    main()
