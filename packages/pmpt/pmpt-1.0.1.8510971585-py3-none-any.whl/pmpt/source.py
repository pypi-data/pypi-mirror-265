import uuid
from moyanlib import jsons
import os
from rich.table import Table
from . import util

def line_search(li, val):
    n = 0
    for i in li:
        print(i)
        if i['id'] == val:
            return i,n
        n += 1
    return None
    
def add(url,priority):
    sourceList = jsons.load(open(os.path.join(util.dirs.user_config_dir,'Source.json')))
    if url in sourceList:
        util.console.print('❌ [red]The source already exists[/red]')
        exit(1)
    sourceList.append({
        'url':url,
        'id':str(uuid.uuid4())[:8],
        'priority':priority
        
    })
    jsons.dump(sourceList,open(os.path.join(util.dirs.user_config_dir,'Source.json'),'w'))
  
    
def lists():
    sourceList = jsons.load(open(os.path.join(util.dirs.user_config_dir,'Source.json')))
    table = Table(show_header=True)
    table.add_column("ID",width=6)
    table.add_column('Priority',width=8)
    table.add_column('URL',width=25)
    
    for i in sourceList:
        table.add_row(
            i['id'],
            str(i['priority']),
            i['url']
        )
    util.console.print(table)
    
def remove(ids,yes):
    if not ids:
        lists()
        ids = util.console.input('Please enter the source sequence number to be deleted:')
        
    sourceList:list = jsons.load(open(os.path.join(util.dirs.user_config_dir,'Source.json')))
    source,n = line_search(sourceList,ids)

    if not source:
        util.console.print('❌ [red]The source for this ID does not exist[/red]')
    
    while True: # 是否允许安装
        if yes:
            break
               
        ye = util.console.input('Are you sure you want to delete? [Y/n]: ')
            
        if ye.lower() == 'y':
            break
        elif ye.lower() == 'n':
            util.console.print('🛑 [red]The user exited the program[/red]')
            exit(1)
        else:
            continue
            
    sourceList.remove(source)
    jsons.dump(sourceList,open(os.path.join(util.dirs.user_config_dir,'Source.json'),'w'))
  
def modify(ids,key,val):
    sourceList:list = jsons.load(open(os.path.join(util.dirs.user_config_dir,'Source.json')))
    source,n = line_search(sourceList,ids)
    if not source:
        util.console.print('❌ [red]The source for this ID does not exist[/red]')
    if key not in ['url','priority']:
        util.console.print('❌ [red]The item is not allowed to be modified or does not exist.[/red]')
    sourceList[n][key] = val
    jsons.dump(sourceList,open(os.path.join(util.dirs.user_config_dir,'Source.json'),'w'))