#pylint:disable=W0622
import os
from subprocess import Popen
import sys
import pathlib
import dill
from rich.console import Console
import time
import subprocess
from moyanlib import jsons
from platformdirs import PlatformDirs

dirs = PlatformDirs("PMPT", "MoYan")
IndexList = []
console = Console()

def getVer(baseVar):
    baseVar = baseVar + '.' + os.environ.get('GITHUB_RUN_ID', str(int(time.time()))[:6])
    return baseVar
    
__version__ = getVer('1.0.1')
def init():
    os.makedirs(dirs.user_data_dir,exist_ok=True)
    os.makedirs(os.path.join(dirs.user_data_dir,'Index'),exist_ok=True)
    os.makedirs(dirs.user_config_dir,exist_ok=True)
    os.makedirs(dirs.user_cache_dir,exist_ok=True)
    
def bubbleSort(arr):
    for i in range(1,len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j]['priority'] < arr[j+1]['priority']:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def loadIndex():
    '''
    加载索引
    '''
    sourceList = jsons.load(open(os.path.join(dirs.user_config_dir,'Source.json')))
    sourceList = bubbleSort(sourceList)
    for source in sourceList:
        if not os.path.exists(os.path.join(dirs.user_data_dir,'Index',source['id']+'.pidx')):
            console.print(f'⚠️ [yellow]{source["url"]} did not create an index.[/yellow]')
            continue
        IndexFile = dill.load(open(os.path.join(dirs.user_data_dir,'Index',source['id']+'.pidx'),'rb')) # 加载索引
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
        console.print('Command to be run:',' '.join(Command))
    
    runClass = Popen(Command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for line in iter(runClass.stdout.readline, b''):
        # 在这里你可以对每一行输出进行处理
        line = line.decode('utf-8').strip()  # 将字节转换为字符串并去除换行符
        console.print(line) 
    runClass.communicate()
    return runClass

    
