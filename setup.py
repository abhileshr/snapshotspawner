from setuptools import setup

setup(
    name='snapshotspawner',
    version='0.1',
    author='Abhilesh Ramteke',
    author_email='abhilesh@hotmail.com',
    description='snapshotspawner is a tool to manage AWS EC2 snapshots',
    license='GPLv3+',
    packages=['shotty'],
    url='https://github.com/abhileshr/snapshotspawner',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',
)
