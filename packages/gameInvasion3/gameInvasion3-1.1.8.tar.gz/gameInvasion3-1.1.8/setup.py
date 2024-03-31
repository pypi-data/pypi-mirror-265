from setuptools import setup, find_packages

with open('requirements.txt',encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='gameInvasion3',
    version='1.1.8',
    url='https://github.com/MaoJiayang/gameInvasion3',
    author='Jiayang Mao',
    author_email='Nucleon_17th@njust.edu.cn',
    description='a python game engine for my 2D game development',
    packages=find_packages(),  
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'gameInvasion3=invasion_game_demo.main:main', 
        ],
    },

)