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

##########Main Group for snapshots##########
@click.group()
def cli():
    "Shotty manages snapshots"

##########Sub Group for snapshots##########
@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

##List Snapshots Command
@snapshots.command('list')
@click.option('--owner', default=None,
    help="Only snapshots for owner (tag Owner:<name>)")
def list_snapshots(owner):
    "List EC2 snapshots"

    instances = filter_instances(owner)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime('%c')
                )))

###########Sub Group for volumes##########
@cli.group('volumes')
def volumes():
    """Commands for volumes"""

##List Volumes Command
@volumes.command('list')
@click.option('--owner', default=None,
    help="Only volumes for owner (tag Owner:<name>)")
def list_volumes(owner):
    "List EC2 volumes"

    instances = filter_instances(owner)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
            v.id,
            i.id,
            v.state,
            str(v.size) + ' GiB',
            v.encrypted and 'Encrypted' or 'Not Encrypted'
            )))
    return

##########Creating Group for instances##########
@cli.group('instances')
def instances():
    """Commands for instances"""

##snapshot Command
@instances.command('snapshot',
    help="Create snapshots of all volumes")
@click.option('--owner', default=None,
    help="Only instances for owner (tag Owner:<name>)")
def create_snapshots(owner):
    "Create snapshots for EC2 instances"

    instances = filter_instances(owner)

    for i in instances:
        print('Stopping {0}...'.format(i.id))

        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print(' Creating snapshot of {0}'.format(v.id))
            v.create_snapshot(Description='Created by SnapshotSpawner')

        print('Starting {0}'.format(i.id))

        i.start()
        i.wait_until_running()

    print('Job is done!')

    return

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
    cli()
