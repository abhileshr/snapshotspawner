# snapshotspawner
A demo project that uses Python for managing EC2 instances

## About
This demo project uses Boto3 to manage AWS EC2 instance snapshots

##Configuring
shotty uses the configuration file created by the AWS CLI e.g.

```
aws configure --profile shotty

pwd
pip3 install pipenv
pipenv --three
pipenv install boto3
pipenv install -d ipython
```

## Running
`pipenv run "python shotty/shotty.py <command> <--owner=OWNER>"`
*command* is list, start or stop
*owner* is optional
