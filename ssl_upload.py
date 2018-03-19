from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import sys
import pprint
import requests
from F5_Stats import F5_Stats
from f5.bigip.contexts import TransactionContextManager
import time


mgmt = ManagementRoot("192.168.109.130", "admin", "pass")

#Works, files in directory ran script from. uploads files to /var/config/rest/downloads/
#Replaces existing files in /var/config/rest/downloads/ if same name

cert = 'ssl-upload.com.crt'
key = 'ssl-upload.com.key'
chain = 'go-daddy.crt'
domain = 'sslupload.com'

mgmt.shared.file_transfer.uploads.upload_file('ssl-upload.com.crt')
print('Uploaded cert file: {}'.format(cert))
mgmt.shared.file_transfer.uploads.upload_file('ssl-upload.com.key')
print('Uploaded key file: {}'.format(key))
mgmt.shared.file_transfer.uploads.upload_file('go-daddy.crt')
print('Uploaded chain file: {}'.format(chain))
#
## install cert/key to devices
newkey = mgmt.tm.sys.file.ssl_keys.ssl_key.create(name='{0}.key'.format(domain),sourcePath='file:/var/config/rest/downloads/{0}'.format(key))
print('Installed cert file: {}'.format(cert))
newcert = mgmt.tm.sys.file.ssl_certs.ssl_cert.create(name='{0}.crt'.format(domain),sourcePath='file:/var/config/rest/downloads/{0}'.format(cert))
print('Installed key file: {}'.format(key))
chain = mgmt.tm.sys.file.ssl_certs.ssl_cert.create(name='{0}'.format(chain),sourcePath='file:/var/config/rest/downloads/{0}'.format(chain))
print('Installed chain file: {}'.format(chain))
#Create new ssl profile with uploaded certs

time.sleep(3)

new_profile = {
    'name': '/Common/{0}'.format(domain),
    'cert': '/Common/{0}.crt'.format(domain),
    'key': '/Common/{0}.key'.format(domain),
    'chain': '/Common/{}'.format(chain),
    'defaultsFrom': '/Common/clientssl'
    }

mgmt.tm.ltm.profile.client_ssls.client_ssl.create(**new_profile)
print('Created ssl profile: {}'.format(domain))