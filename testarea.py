from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import sys
import requests
import pprint
import ipaddress

mgmt = ManagementRoot("192.168.109.130", "admin", "pass")






######### NETWORK MAP ##########

f5_map = {}

virtuals = mgmt.tm.ltm.virtuals.get_collection()

for line in virtuals:    
    virt = mgmt.tm.ltm.virtuals.virtual.load(partition=line.partition, name=line.name)
    pprint.pprint(virt.pool)
    f5_map[line.name] = {}
#    for vip in virt:
#        pprint.pprint(vip.raw)
#        f5_map[line.name][v]

pprint.pprint(f5_map)

pool_members = [['192.168.5.5:80', '192.168.12.5:80'], ['192.168.5.5:443', '192.168.12.5:443']]


#cciphers = b.tm.util.clientssl_ciphers.exec_cmd('run', utilCmdArgs='TLSv1+HIGH:!SSLv2:!aNULL:!eNULL:@STRENGTH')



########### POOL DATA

#pools = []
#
#pool = ''
##
#all_pools = mgmt.tm.ltm.pools.get_collection()
#
#pool_data = mgmt.tm.ltm.pools.pool.load(partition='Common', name=pool)
#poolstats = pool_data.members_s.get_collection()
#output = {}
#
#for line in all_pools:
#    #pprint.pprint(line.raw)
#    pools.append(line.name)
#
#print(pools)
#
##or line in poolstats:
##   print(line.name)
##
##or member in poolstats:
##   member_stats = Stats(member.stats.load())
##   output['nodename'] = member_stats.stat.nodeName
##   output['CurrentConns'] = member_stats.stat.serverside_curConns
##   output['TotalConns'] = member_stats.stat.serverside_totConns
##   output['MaxConns'] =  member_stats.stat.serverside_maxConns
##   output['Availability'] = member_stats.stat.status_availabilityState
###    pprint.pprint(member_stats.stat)
##
#pprint.pprint(output)
#


## list self IPs
#ip = mgmt.tm.net.selfips.get_collection()
#
#for line in ip:
#    pprint.pprint(line.address)
#
## list arps
#
#arps = mgmt.tm.net.arps.get_collection()
#
#for line in arps:
#    print(line)
#

#    print(member_stats.stat.status_availabilityState)
#    print(member_stats.stat.serverside_curConns)

#print.pprint(pooloutput)
#pprint.pprint(member_stats.raw)
