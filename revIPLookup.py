#!/usr/bin/env python3

from colored import fg, bg, attr, stylize
from ipdetector import ipCategorizer
import ipaddress
import requests
import argparse
import sys
import re

class revIPLookup:
    default = fg(246)
    green = fg(34) + attr('bold')
    yellow = fg(221)
    reset = attr('reset')
    dark_yellow = fg(214)

    error = fg('red') + '[!] ' + default      
    detail = fg(220) + '[*] ' + default         
    fail = fg('red') + '[-] ' + default         
    success = fg('green') + '[+] ' + default    
    event = fg(26) + '[*] ' + default           
    debug = fg('magenta') + '[%] ' + default    
    notification = fg(246) + '[-] ' + default

    __author__= default + '''
############################################################
     _____      _ ____  _     ___   ___  _                
 _ _|___ /_   _/ |  _ \| |   / _ \ / _ \| | ___   _ _ __  
| '__||_ \ \ / / | |_) | |  | | | | | | | |/ / | | | '_ \ 
| |  ___) \ V /| |  __/| |__| |_| | |_| |   <| |_| | |_) |
|_| |____/ \_/ |_|_|   |_____\___/ \___/|_|\_\\\__,_| .__/ 
                                                   |_|
############################################################
    [+] Author : 1uffyD9
    [+] Github : https://github.com/1uffyD9
############################################################
'''

    def __init__(self,):
        try:
            print (self.__author__, end='')     
            self.main()

        except KeyboardInterrupt:
            sys.exit('\n' + self.error + "Keyboard inturruption occurd, exiting the program.." + self.reset)

    def get_args(self,):
        parser = argparse.ArgumentParser(description="revIPLookup will give you domain name(s) for the IP(s) you're given")
        parser.add_argument('-i', '--ip', type=str, help='specify the IP address or range')
        parser.add_argument('-f', '--file', type=str, help='specify the IP/IP list range')
        
        return parser.parse_args()

    def main(self,):
        ip, ip_file = vars(self.get_args()).values()

        if ip or ip_file:
            if ip_file:
                try:
                    ip_file = open(ip_file, 'rb').readlines()
                    for ip in ip_file:
                        ip = ip.decode('utf-8').rstrip()
                        if ipCategorizer(ip):
                            if ipCategorizer(ip)[0] == 1 or ipCategorizer(ip)[0] == 3:
                                if ipCategorizer(ip)[0] == 1:
                                    self.reverseIPlookup(ip)
                                else:
                                    for ip in list(str(i) for i in ipaddress.ip_network(ip).hosts()):
                                        self.reverseIPlookup(ip) 
                            else:
                                print (self.event + "Private IP/IP range ({}) detected".format(ip))
                    sys.exit()

                except IOError as e:
                    sys.exit(self.error + str(e).split("] ")[1])

            if ip:
                if ipCategorizer(ip):
                    if ipCategorizer(ip)[0] == 1 or ipCategorizer(ip)[0] == 3:
                        if ipCategorizer(ip)[0] == 1:
                            self.reverseIPlookup(ip)
                        else:
                            for ip in list(str(i) for i in ipaddress.ip_network(ip).hosts()):
                                self.reverseIPlookup(ip) 
                    else:
                        sys.exit(self.error + "Private IP/IP range detected")

        else:
            sys.exit(self.error + "one of the following arguments are required: -i/--ip, -f/--file")

    def reverseIPlookup(self, ip):
        print('\r' + self.debug + "Searching a record for " + self.dark_yellow + ip + self.default + ' ' * 10, end='\r')
        url = "https://api.hackertarget.com/reverseiplookup/?q=" + ip
        try:
            req = requests.get(url)
            if "No DNS" not in req.text:
                print('\r' + self.success + "Found a record for " + self.green + ip + ' ' * 20 + self.default)
                for i in re.split('\n', req.text):
                    if ip not in i and i.strip():
                        print ('\t' + self.success + i + self.reset)
        except requests.exceptions.RequestException as e:
            sys.exit(self.error + "Something going wrong with the connection.Please check the connectivity" + self.reset)

revIPLookup()

