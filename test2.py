from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import sys
import pprint
import requests
from F5_Stats import F5_Stats
from f5.bigip.contexts import TransactionContextManager
import time


mgmt = ManagementRoot("192.168.109.130", "admin", "pass")

