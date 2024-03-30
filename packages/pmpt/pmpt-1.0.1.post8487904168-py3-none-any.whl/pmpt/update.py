import requests
from moyanlib import jsons
from tqdm import tqdm
import dill
import os
import urllib.parse as urlparse
from hashlib import sha256
from .util import dirs

def getSourceID(url):
    '''
    获取源id
    '''
    url = urlparse.urlparse(url)
    SourceID_Str = url.netloc + url.path # 取主机名和路径
    sha = sha256()
    sha.update(SourceID_Str.encode())
    return sha.hexdigest()[:8] # 取前八位
    
class Index:
    def __init__(self,indexurl):
        self.packageList = {}
        self.IndexURL = indexurl
        self.number = 0
        
    def addPackage(self, name):
        self.packageList[name] = 'H'
        self.number += 1
    
def getIndex(url):
    req = requests.get(url) # 请求HTML
    HTMLIndex = req.text

    ClassIndex = Index(url)

    print('Start parsing the HTML index for this source.')
    for line in tqdm(HTMLIndex.split('\n')):
        # 提取并筛选标签
        line_list = line.split('>') 
        if len(line_list) > 1 and '<a ' in line:
            package_name = line_list[1].split('<')[0]
            
            ClassIndex.addPackage(package_name) # 添加包
    
    print('This source has a total of', ClassIndex.number,'packages.') 
    print('Start saving the index for this source.')     
    dill.dump(ClassIndex,open(f'{dirs.user_data_dir}/Index/{getSourceID(url)}.pidx','wb'))

def getAllIndex():
    '''
    SourceList = [
        'https://pypi.tuna.tsinghua.edu.cn/simple',
        'https://mirrors.bfsu.edu.cn/pypi/web/simple/'
    ]
    '''
    SourceList = jsons.load(open(os.path.join(dirs.user_config_dir,'Source.json'))) # 加载源列表
    if len(SourceList) < 1:
        print('You have not configured any sources.')
        exit(1)
        
    for url in SourceList: # 遍历源列表
        print('Start downloading index from', url)
        getIndex(url)
        print()
        
