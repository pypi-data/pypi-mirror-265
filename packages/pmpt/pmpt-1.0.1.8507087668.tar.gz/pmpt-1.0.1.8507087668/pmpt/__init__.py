import click
from . import update as updates
from . import util
from moyanlib import jsons
from . import source as sou
from . import install as installs 
from . import search as searchs

@click.group()
def cli():
    try:
        import pip
    except ImportError:
        util.console.print('❌ [red]pip module not found![/red]')
        exit(1)
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
@click.option('--command','-c',is_flag=True,default=False)
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
@click.option('--priority','-p',default=1,type=int)
def add(*args,**kwargs):
    sou.add(*args,**kwargs)
    
@source.command(name='list')
def lists():
    sou.lists()
    
@source.command(name='remove')
@click.argument('ids',default=None,required=False)
@click.option('-y','--yes',is_flag=True,default=False)
def removes(*args,**kwargs):
    sou.remove(*args,**kwargs)
       
@source.command(name='modify')
@click.argument('ids')
@click.argument('key')
@click.argument('val')
def modifys(*args,**kwargs):
    sou.modify(*args,**kwargs)
    
if __name__ == '__main__':
    cli()