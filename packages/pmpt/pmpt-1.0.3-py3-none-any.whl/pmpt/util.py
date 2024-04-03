#pylint:disable=W0622
import os
from subprocess import Popen
import sys
import dill
from rich.console import Console
from loguru import logger
import subprocess
from moyanlib import jsons
from platformdirs import PlatformDirs

dirs = PlatformDirs("PMPT", "MoYan")
IndexList = []
console = Console()

def getVer(baseVar):
    baseVar = baseVar # + '.' + os.environ.get('GITHUB_RUN_ID', str(int(time.time()))[:6])
    logger.info('PMPT '+baseVar)
    return baseVar

def GlobalDecorator(frame, event, arg):
    if event == 'call': 
        try:
            func_name = frame.f_code.co_name
            module_name = frame.f_globals['__name__']
            package_name = module_name.split('.')[0]  # 假设包名为模块名的第一部分
            if package_name == 'pmpt':
                logger.trace(f"调用函数 {module_name}.{func_name}")
        except:
            pass
    return GlobalDecorator
    
sys.settrace(GlobalDecorator) 
   
logger.remove()
logger.add(
    os.path.join(dirs.user_data_dir,'log.log'),
    level='TRACE',
)

__version__ = getVer('1.0.3')


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
            logger.warning(source['url']+'没有索引')
            console.print(f'⚠️ [yellow]{source["url"]} did not create an index.[/yellow]')
            continue
        logger.debug(source)
        IndexFile = dill.load(open(os.path.join(dirs.user_data_dir,'Index',source['id']+'.pidx'),'rb')) # 加载索引
        IndexList.append(IndexFile)
    if len(IndexList) == 0:
        
        raise FileNotFoundError('No index. Run "pmpt update" first to update the index')

def runpip(command,other=None,dbg=False,out=True) -> Popen:
    '''
    运行pip
    '''
    logger.trace('调用runpip')
    if not other:
        other = []
    baseCommand = [sys.executable,'-m','pip']
    baseCommand.append(command)
    
    Command = baseCommand + other
    if dbg:
        console.print('Command to be run:',' '.join(Command))
    logger.debug(' ',)
    runClass = Popen(Command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if out:
        for line in iter(runClass.stdout.readline, b''):
            # 在这里你可以对每一行输出进行处理
            line = line.decode('utf-8').strip()  # 将字节转换为字符串并去除换行符
            console.print(line) 
        if runClass.returncode != 0:
            console.print(runClass.stderr.read().decode())
        runClass.communicate()
    else:
        runClass.wait()
    return runClass

    
