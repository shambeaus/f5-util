from f5.bigip import ManagementRoot
import sys
from F5_Config import F5_Config
import requests
import pprint


mgmt = ManagementRoot("192.168.109.130", "admin", "pass")


partition = 'Common'
pool_members = ['192.168.5.5:80', '192.168.12.5:80']
public_IP = '12.7.81.55'
nat_IP = '192.168.51.5'
port = '80'
vip_name = 'VS-{}-{}'.format(public_IP,port)
destination_IP = '{}:{}'.format(nat_IP,port)
pool_name = 'POOL-{}-{}'.format(public_IP,port)

virtuals_data = mgmt.tm.ltm.virtuals.get_collection()
pools_data = mgmt.tm.ltm.pools.get_collection()


f5_config = F5_Config()




#Create new VIP

f5_config.qc_vip(virtuals_data, pools_data, vip_name, destination_IP, pool_name)

pooloutput = f5_config.create_new_pool(mgmt, partition, pool_name, pool_members)
vipoutput = f5_config.create_new_vip(mgmt, virtuals_data, partition, vip_name, destination_IP, pool_name)




#pprint.pprint(pooloutput)
#pprint.pprint(vipoutput)
