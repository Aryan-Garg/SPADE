from setuptools import setup

setup(
    name='slackTools',
    version='0.1.0',    
    description='Connect your research to Slack!',
    url='https://github.com/lvsn/slackTools',
    author='Ian Maquignaz',
    author_email='ian.maquignaz.1@ulaval.ca',
    license="LGPLv3",
    packages=['slackTools'],
    install_requires=['slack_sdk>=2.0'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
