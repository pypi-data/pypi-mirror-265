from . import util

def search(name):
    util.loadIndex() #加载索引
    
    for Index in util.IndexList:
        dt = Index.packageList.get(name,None)
        if dt:
            return Index.IndexURL
        
def main(packlist,upgrade,reads,force_reinstall,ignore_requires_python,yes):
    
    if reads: # 从文件读取列表
        f = open(packlist[0])
        packlist = f.read().split('\n')
    
    packsInfo = {}
    print('Start installing these packages')
    print('Start looking for package')
        
    for rawpack in packlist: # 解析指定了版本的包名
        if '==' in rawpack:
            pack = rawpack.split('==')[0]
        elif '>=' in rawpack:
            pack = rawpack.split('>=')[0]
        elif '<=' in rawpack:
            pack = rawpack.split('<=')[0]
        elif '<' in rawpack:
            pack = rawpack.split('<')[0]
        elif '>' in rawpack:
            pack = rawpack.split('>')[0]
        else:
            pack = rawpack
            
        
        result = search(pack.lower()) # 转小写并获取源地址
        packsInfo[pack] = [result,rawpack]
     
    canInstallPack = []   
    for k,v in packsInfo.items():
        if not v:
            print('Unable to find', k)
        else:
            print(f'Find {k} from {v[0]}')
            canInstallPack.append(k)
    
    print('Will install',', '.join(canInstallPack))
    
    while True: # 是否允许安装
        if yes:
            break
            
        ye =input('Are you sure you want to install? (y/n)')
        
        if ye.lower() == 'y':
            break
        elif ye.lower() == 'n':
            print('User Cancels Installation')
            exit()
        else:
            continue
            
    print('Start calling pip')        
    for pack in canInstallPack:
        # 构建命令
        args = [ '-i', packsInfo[pack][0]] # 指定源
            
        if upgrade: # 升级
            args.append('-U')
        if force_reinstall: # 强制重新安装
            args.append('--force-reinstall')
        if ignore_requires_python: # 忽略Python版本
            args.append('--ignore-requires-python')
                
        args.append(packsInfo[pack][1])
        ret = util.runpip('install',args) # 运行pip
        
        if ret.returncode != 0: #是否执行完毕
            print('Failed to install.')
            exit()
        print('Installation completed')
        
            
        