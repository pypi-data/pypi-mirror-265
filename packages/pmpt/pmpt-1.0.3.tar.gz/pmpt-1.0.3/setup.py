from setuptools import setup, find_packages
from setuptools.command.install import install 
import os
from pmpt import util

class CustomInstallCommand(install): 
    def run(self): 
        install.run(self) # 在安装过程中执行你想要的代码 
        dirs = util.dirs
        os.makedirs(dirs.user_data_dir,exist_ok=True)
        os.makedirs(os.path.join(dirs.user_data_dir,'Index'),exist_ok=True)
        os.makedirs(dirs.user_config_dir,exist_ok=True)
        os.makedirs(dirs.user_cache_dir,exist_ok=True)
        open(os.path.join(dirs.user_config_dir,'Source.json'),'w').write('["https://pypi.org/simple/"]')
        open(os.path.join(dirs.user_config_dir,'api.url'),'w').write('https://pypi.org/pypi/{}/json')


setup(
    name='pmpt',  # 包的名称
    version=util.__version__,  # 版本号
    packages=find_packages(),  # 包含的包
    author='MoYan',  # 作者
    author_email='moyan@moyanjdc.top',  # 作者邮箱
    description='A Python Package Advanced Manager',  # 包的简要描述
    long_description=open("readme.md").read(),  # 包的详细描述
    long_description_content_type='text/markdown',  # 描述的内容类型
    classifiers=[  # 包的分类信息
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    setup_requires = ['platformdirs'],
    install_requires=open('requirements.txt').read().split('\n'),
    entry_points={
        'console_scripts': [
            'pmpt=pmpt:cli',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    }
)
