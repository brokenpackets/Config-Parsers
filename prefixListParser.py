#!/usr/bin/python
from jsonrpclib import Server
import json
import ssl
import re

#CREDS
user = "admin"
passwd = "Arista"
ssl._create_default_https_context = ssl._create_unverified_context

#VARIABLES
switchIP = '192.168.255.7'
prefixListName = 'TESTPrefixList'

"""
Parser to gather prefix-list from device and find next highest sequence number.
Uses Arista eAPI to collect this information.
"""

def main():

  #SESSION SETUP FOR eAPI TO DEVICE
  url = "https://%s:%s@%s/command-api" % (user, passwd, switchIP)
  ss = Server(url)
  permit_regex = re.compile('seq ([0-9]{1,6}) permit.*')
  deny_regex = re.compile('seq ([0-9]{1,6}) deny.*')

  #CONNECT TO DEVICE
  prefixList = ss.runCmds( 1, ['show running-config'])[0]['cmds']\
  ['ip prefix-list '+prefixListName]['cmds']
  listNumbers = []
  for item in prefixList:
      if permit_regex.match(item):
          listNumbers.append(int(permit_regex.match(item).group(1)))
      if deny_regex.match(item):
          listNumbers.append(int(deny_regex.match(item).group(1)))
  print max(listNumbers)+10


if __name__ == "__main__":
  main()
