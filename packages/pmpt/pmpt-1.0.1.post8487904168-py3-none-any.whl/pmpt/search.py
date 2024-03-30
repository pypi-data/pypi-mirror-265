import requests
from . import util
from moyanlib import jsons
from .install import search
import os
def main(name,allinfo,api_url):
    if not search(name):
        print('The package does not exist')
        exit()
        
    if not api_url:
        api_url = open(os.path.join(util.dirs.user_config_dir,'api.url')).read()
    
    req = requests.get(api_url.format(name))
    if req.status_code == 404:
        print('The package does not exist')
        exit()
    elif req.status_code != 200:
        print('Server Error!')
        print('Error Code:',req.status_code)
        exit()
    
    
    packageInfo =  jsons.loads(req.text)  
    if not allinfo:
        print('Package Name:',packageInfo['info']['name'])
        print('Version:',packageInfo['info']['version'])
        print('Author:',packageInfo['info']['author'])
        print('Summary:',packageInfo['info']['summary'])
        print('Keywords:',packageInfo['info']['keywords'])
        print('License:',packageInfo['info']['license'])
        print('Dependent Library:',', '.join(packageInfo['info']['requires_dist']))
    elif allinfo:
        for k,v in packageInfo['info'].items():
            print(f'{k}: {v}')
    