from f5.bigip import ManagementRoot
import sys

class F5_Config(object):


    ###################################
    ## Virtual Config
    ###################################


    def create_new_vip(self, mgmt, virtuals_data, part, vip_name, destination_IP, pool_name):
        if mgmt.tm.ltm.virtuals.virtual.exists(partition=part, name=vip_name):
            print('Virtual already exists')
            sys.exit()        
        else:
            virtual = mgmt.tm.ltm.virtuals.virtual.create(partition=part, name=vip_name, ipProtocol='tcp', pool=pool_name, destination=destination_IP)
        if mgmt.tm.ltm.virtuals.virtual.exists(partition=part, name=vip_name):
            print('Successfully created VIP : ' + vip_name)
            #Collect raw data of VIP created
            output = virtual.raw
            return output
        else:
            print('something is frigged')

        #def delete_vip

    ###################################
    ## Pool Config
    ###################################

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
            #collect raw data of pool created
            output.append(pool.raw)
        else:
            print('something is frigged')
        # Add members to pool
        print('Adding members to pools')
        if pool_members:
            for member in pool_members:
                pool_member = pool.members_s.members.create(partition=part, name=member)
                print(' Added member ' + member)
                #collect raw data of pool members created
                output.append(pool_member.raw)         
        else:
            print('no members provided')
            return output
        return output

    def add_members(self, pool_name, member_list):
        pool = mgmt.tm.ltm.pools.pool.load(name=pool_name)
        members =  pool.members_s.get_collection()

        for m in member_list:
            if pool.members_s.members.exists(partition='Common', name=m):
                print('Pool member ' + m + ' already exists')
                sys.exit()
            else:
                member = pool.members_s.members.create(partition='Common', name=m)
                print('Member {} added to pool {}'.format(m,pool_name))


    def replace_members(self, pool_name, member_list):
        pool = mgmt.tm.ltm.pools.pool.load(name=pool_name)

        members =  pool.members_s.get_collection()
        existing_members = set([m.name for m in members])
        new_members = set(member_list)

        add_members = new_members - existing_members
        remove_members = existing_members - new_members

        for m in add_members:
            member = pool.members_s.members.create(partition='Common', name=m)
            print('Added pool member ' + m)

        for m in remove_members:
            member = pool.members_s.members.load(partition='Common', name=m)
            member.delete()
            print('Removed Pool member ' + m)



    #def pool_member status():

    #def delete_pool:

        

    ###################################
    ## Quality Check
    ###################################

    def qc_vip(self, virtuals_data, pools_data, vip_name, destination_IP, pool_name, selfip_data, nat_IP):
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
        for line in selfip_data:
            if nat_IP in line.address:
                print('Nat IP ' + nat_IP + ' already used as Self IP')
                sys.exit()


    def save_sys_config(self, mgmt):
        #need to figure out how to get status of command
        output = mgmt.tm.sys.config.exec_cmd('save')
        return output



