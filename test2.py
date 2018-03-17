from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import sys
import pprint

def get_pool_stats(p_name, p_partition):
    #List for stats from all members 
    output = []
    """Return all pool stats object (dict of dicts)"""
    #load pool and member information
    pool_data = mgmt.tm.ltm.pools.pool.load(name=p_name, partition=p_partition)
    poolstats = pool_data.members_s.get_collection()
    for member in poolstats:
        #stats module needs to be used here to work with the stats.load() returned data
        output.append(Stats(member.stats.load()))
    return output


pool = 'POOL-TOWN-BURG'


mgmt = ManagementRoot("192.168.109.130", "admin", "pass")
POOL_STATS = get_pool_stats(pool, 'Common')



print('Pool Name : ' + pool)
print('--------------------')
print('--------------------')

i = 0
while i < len(POOL_STATS):
#   Use .stat to get all available values 
#   pprint.pprint(POOL_STATS[i].stat)
    print('Pool member Name : ' + POOL_STATS[i].stat.nodeName['description'])
    print('Pool member monitor : ' + POOL_STATS[i].stat.monitorRule['description'])
    print('Pool monitor status : ' + POOL_STATS[i].stat.monitorStatus['description'])
    print('Pool availability state : ' + POOL_STATS[i].stat.status_availabilityState['description'])
    print('Pool member Current Conns : ' + str(POOL_STATS[i].stat.serverside_curConns['value']))
    print('Pool member Total Conns : ' + str(POOL_STATS[i].stat.serverside_totConns['value']))
    print('Pool member Max Conns : ' + str(POOL_STATS[i].stat.serverside_maxConns['value']))
    print('--------------------')
    i += 1
