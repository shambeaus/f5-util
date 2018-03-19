from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import sys
import pprint

class F5_Stats(object):

    def get_pool_stats(self, mgmt, pool_name, part):
        #List for stats from all members 
        output = []
        """Return all pool stats object (dict of dicts)"""
        #load pool and member information
        pool_data = mgmt.tm.ltm.pools.pool.load(name=pool_name, partition=part)
        poolstats = pool_data.members_s.get_collection()
        for member in poolstats:
            #stats module needs to be used here to work with the stats.load() returned data
            output.append(Stats(member.stats.load()))
        return output


    def format_pool_stats(self, pool, pool_stats):
        print('Pool Name : ' + pool)
        print('--------------------')
        print('--------------------')

        i = 0
        while i < len(pool_stats):
#           Use .stat to get all available values 
#           pprint.pprint(POOL_STATS[i].stat)
            print('Pool member Name : ' + pool_stats[i].stat.nodeName['description'])
            print('Pool member monitor : ' + pool_stats[i].stat.monitorRule['description'])
            print('Pool monitor status : ' + pool_stats[i].stat.monitorStatus['description'])
            print('Pool availability state : ' + pool_stats[i].stat.status_availabilityState['description'])
            print('Pool member Current Conns : ' + str(pool_stats[i].stat.serverside_curConns['value']))
            print('Pool member Total Conns : ' + str(pool_stats[i].stat.serverside_totConns['value']))
            print('Pool member Max Conns : ' + str(pool_stats[i].stat.serverside_maxConns['value']))
            print('--------------------')
            i += 1


    def HA_status(self,mgmt):
        x = Stats(mgmt.tm.cm.failover_status.load())
        output = x.stat['status']['description']
        return output


