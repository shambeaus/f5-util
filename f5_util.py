from f5.bigip import ManagementRoot
import sys
from F5_Config import F5_Config
from F5_Stats import F5_Stats
import time
import requests
import pprint
import argparse


f5_config = F5_Config()
f5_stats = F5_Stats()

mgmt = ManagementRoot("192.168.109.130", "admin", "pass", token='true')


#partition = 'Common'
#pool_members = ['192.168.5.5:80', '192.168.12.5:80']
#public_IP = '13.7.55.25'
#nat_IP = '192.162.5.62'
#port = '80'
#vip_name = 'VS-{}-{}'.format(public_IP,port)
#destination_IP = '{}:{}'.format(nat_IP,port)
#pool_name = 'POOL-{}-{}'.format(public_IP,port)



public_IP = '15.1.59.166'
nat_IP = '192.255.6.39'
pool_members = [['192.168.5.5:80', '192.168.12.5:80', '192.168.12.99:80'], ['192.168.5.5:443', '192.168.12.5:443',  '192.168.55.5:443']]




partition = 'Common'
port = ['80','443']
vip_name = ['VS-{}-{}'.format(public_IP,port[0]), 'VS-{}-{}'.format(public_IP,port[1])]
destination_IP = ['{}:{}'.format(nat_IP,port[0]) , '{}:{}'.format(nat_IP,port[1])]
pool_name = ['POOL-{}-{}'.format(public_IP,port[0]) , 'POOL-{}-{}'.format(public_IP,port[1])]



###################################
## DATA COLLECTION
###################################

virtuals_data = mgmt.tm.ltm.virtuals.get_collection()
pools_data = mgmt.tm.ltm.pools.get_collection()
selfip_data = mgmt.tm.net.selfips.get_collection()
arp_data = mgmt.tm.net.arps.get_collection()



###################################
## Configuration
###################################


#Create new VIP

print('Performing quality check on provided IPs')
print('')

f5_config.qc_vip(virtuals_data, pools_data, vip_name[0], destination_IP[0], pool_name[0], selfip_data, nat_IP)
f5_config.qc_vip(virtuals_data, pools_data, vip_name[1], destination_IP[1], pool_name[1], selfip_data, nat_IP)
time.sleep(3)
print('No issues found, creating VIPs')
print('')
time.sleep(3)

pooloutput = f5_config.create_new_pool(mgmt, partition, pool_name[0], pool_members[0])
vipoutput = f5_config.create_new_vip(mgmt, virtuals_data, partition, vip_name[0], destination_IP[0], pool_name[0])



pooloutput = f5_config.create_new_pool(mgmt, partition, pool_name[1], pool_members[1])
vipoutput = f5_config.create_new_vip(mgmt, virtuals_data, partition, vip_name[1], destination_IP[1], pool_name[1])

#pprint.pprint(pooloutput)
#pprint.pprint(vipoutput)


###################################
## Stat Collection
###################################

#pool_name = ''

#pool_stats = f5_stats.get_pool_stats(mgmt, pool_name, partition)
#f5_stats.format_pool_stats(pool_name, pool_stats)
