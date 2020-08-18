# snapshotspawner
A demo project that uses Python for managing EC2 instances

## Running

This project requires Python 3 and the requests package.

First install pipenv. Then
```
aws configure --profile shotty
pwd
pip3 install pipenv
pipenv --three
pipenv install boto3
pipenv install -d ipython
pipenv run "python meteors/find_meteors.py"
```
