import click
from . import update as updates
from . import util
from moyanlib import jsons
import os
from . import install as installs 
from . import search as searchs
@click.group()
def cli():
    util.init() # 初始化
 
@cli.command(short_help='Update Package Index')
def update():
    # 调用更新函数
    updates.getAllIndex()
    
@cli.command(short_help='Install Python package')
@click.argument('packlist',nargs=-1, required=True)
@click.option('--upgrade','-U',is_flag=True,default=False)
@click.option('--reads', '-r',is_flag=True,default=False)
@click.option('--force-reinstall','-fr',is_flag=True,default=False)
@click.option('--ignore-requires-python','-irp',is_flag=True,default=False)
@click.option('--yes','-y',is_flag=True,default=False)
def install(*args,**kwargs):
    installs.main(*args,**kwargs)
 
@cli.command(name='list',short_help='List all Python packages')
def listp():    
    util.runpip('list') 
    
@cli.command() 
@click.argument('name')
@click.option('--yes','-y',is_flag=True,default=False)
def remove(name,yes):
   args = []
   if yes:
       args.append('-y')
   args.append(name)
   util.runpip('uninstall',args)
   
@cli.command()
@click.argument('name')
@click.option('--allinfo','-a',is_flag=True,default=False)
@click.option('--api-url','-u',default=None)
def search(*args, **kwargs):
    searchs.main(*args,**kwargs)
    
@cli.group()
def source():
    pass
    
@source.command()
@click.argument('url')
def add(url):
    sourceList = jsons.load(open(os.path.join(util.dirs.user_config_dir,'Source.json')))
    if url in sourceList:
        print('The source already exists')
        exit()
    sourceList.append(url)
    jsons.dump(sourceList,open(os.path.join(util.dirs.user_config_dir,'Source.json')))
@source.command(name='list')
def lists():
    sourceList = jsons.load(open(os.path.join(util.dirs.user_config_dir,'Source.json')))
    ids = 1
    for i in sourceList:
        print(str(ids)+'.',i)
if __name__ == '__main__':
    cli()