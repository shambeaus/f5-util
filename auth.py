import requests
import json 
requests.packages.urllib3.disable_warnings()
 
  
def get_token(bigip, url, creds):
    payload = {}
    payload['username'] = creds[0]
    payload['password'] = creds[1]
    payload['loginProviderName'] = 'tmos'
 
    token = bigip.post(url, json.dumps(payload)).json()['token']['token']
    return token

 
hostname = '192.168.109.130'
username = 'admin'
password = 'pass'
 
url_base = 'https://{}/mgmt'.format(hostname)
url_auth = '{}/shared/authn/login'.format(url_base)
   
b = requests.session()
b.headers.update({'Content-Type':'application/json'})
b.auth = (username, password)
b.verify = False
 
token = get_token(b, url_auth, (username, password))
print(token)