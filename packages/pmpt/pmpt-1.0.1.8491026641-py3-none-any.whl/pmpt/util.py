#pylint:disable=W0622
import os
from subprocess import Popen,PIPE
import sys
import pathlib
import dill
from rich import print
import time
from platformdirs import PlatformDirs

dirs = PlatformDirs("PMPT", "MoYan")
IndexList = []
def getVer(baseVar):
    baseVar = baseVar + '.' + os.environ.get('GITHUB_RUN_ID', str(int(time.time()))[:6])
    return baseVar
    
__version__ = getVer('1.0.1')
def init():
    os.makedirs(dirs.user_data_dir,exist_ok=True)
    os.makedirs(os.path.join(dirs.user_data_dir,'Index'),exist_ok=True)
    os.makedirs(dirs.user_config_dir,exist_ok=True)
    os.makedirs(dirs.user_cache_dir,exist_ok=True)

def loadIndex():
    '''
    加载索引
    '''
    if len(IndexList) == 0: # 判断是否为空
        print('🔍 Loading index...')
        IndexDir = pathlib.Path(os.path.join(dirs.user_data_dir,'Index'))
        for i in IndexDir.iterdir(): # 遍历索引文件夹
            IndexFile = dill.load(open(i,'rb')) # 加载索引
            IndexList.append(IndexFile)
        
        if len(IndexList) == 0:
            raise FileNotFoundError('No index. Run "pmpt update" first to update the index')

def runpip(command,other=None,dbg=False) -> Popen:
    '''
    运行pip
    '''
    if not other:
        other = []
    baseCommand = [sys.executable,'-m','pip']
    baseCommand.append(command)
    
    Command = baseCommand + other
    if dbg:
        print('Command to be run:',' '.join(Command))
    
    runClass = Popen(Command)
    runClass.wait()
    return runClass
    