import boto3
import click
## Replacing tag: Project:Valkyrie with Owner:Mac

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

##Common code fn for returning filtered instances
def filter_instances(owner):
    instances = []
    if owner:
        filters = [{'Name':'tag:Owner', 'Values':[owner]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

##Creating Group for instances
@click.group()
def instances():
    """Commands for instances"""

##List Command
@instances.command('list')
@click.option('--owner', default=None,
    help="Only instances for owner (tag Owner:<name>)")
def list_instances(owner):
    "List EC2 instances"

    instances = filter_instances(owner)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Owner', '<No Owner>')
            )))
    return

##Stop Command
@instances.command('stop')
@click.option('--owner', default=None,
    help="Only instances for owner")
def stop_instances(owner):
    "Stop EC2 instances"

    instances = filter_instances(owner)

    for i in instances:
        print('Stopping {0}..'.format(i.id))
        i.stop()
    return

##Start Command
@instances.command('start')
@click.option('--owner', default=None,
    help="Only instances for owner")
def stop_instances(owner):
    "Start EC2 instances"

    instances = filter_instances(owner)

    for i in instances:
        print('Starting {0}..'.format(i.id))
        i.start()
    return

if __name__ == '__main__':
    instances()
