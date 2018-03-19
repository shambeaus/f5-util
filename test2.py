from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import sys
import pprint
import requests
from F5_Stats import F5_Stats

mgmt = ManagementRoot("192.168.109.130", "admin", "pass")

f5_stats = F5_Stats()

version = f5_stats.check_version(mgmt)

if version < '11.1.3':
    print('less than number')


