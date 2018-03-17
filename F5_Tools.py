from f5.bigip import ManagementRoot
import sys

class F5_Tools(object):

    def create_new_pool(self, mgmt, part, pool_name, pool_members):
        output = []
        # Check if there is an existing pool
        if mgmt.tm.ltm.pools.pool.exists(partition=part, name=pool_name):
            print('Pool already exists')
            sys.exit()
        pool = mgmt.tm.ltm.pools.pool.create(partition=part, name=pool_name, monitor='tcp')
        # Verify pool was created
        if mgmt.tm.ltm.pools.pool.exists(partition=part, name=pool_name):
            print('Successfully created pool : ' + pool_name)
            # NEED too append this to the output
            output.append(pool.raw)
        else:
            print('something is frigged')
        # Add members to pool
        print('Adding members to pools')
        if pool_members:
            for member in pool_members:
                pool_member = pool.members_s.members.create(partition=part, name=member)
                print(' Added member ' + member)
                output.append(pool_member.raw)         
        else:
            print('no members provided')
            return output
            sys.exit()
        return output


    def create_new_vip(self, mgmt, virtuals_data, part, vip_name, destination_IP, pool_name):
        if mgmt.tm.ltm.virtuals.virtual.exists(partition=part, name=vip_name):
            print('Virtual already exists')
            sys.exit()        
        else:
            virtual = mgmt.tm.ltm.virtuals.virtual.create(partition=part, name=vip_name, ipProtocol='tcp', pool=pool_name, destination=destination_IP)
        if mgmt.tm.ltm.virtuals.virtual.exists(partition=part, name=vip_name):
            print('Successfully created VIP : ' + vip_name)
            output = virtual.raw
            return output
        else:
            print('something is frigged')

    def qc_vip(self, virtuals_data, pools_data, vip_name, destination_IP, pool_name):
        for line in virtuals_data:
            if vip_name in line.name:
                print('VIP ' + vip_name + ' already exists')
                sys.exit()
            elif destination_IP in line.destination:
                print('Destination IP ' + destination_IP + ' already in use.')
                sys.exit()
        for line in pools_data:
            if pool_name in line.name:
                print('Pool ' + pool_name + ' already in use')
                sys.exit()



#    def update_pool_members(self, mgmt, pool_name, pool_members):
        