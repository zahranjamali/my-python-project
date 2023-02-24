import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

instance_id = "id-xxxxxxxxxxx" #hardcode instance-id here whose volume we have to recover

volumes = ec2_client.describe_volumes( # giving our instance_id and taking volume attached to it as output
    Filters = [
        {
           'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)
instance_volume = volumes['Volumes'][0]
#print(instance_volume)

snapshots = ec2_client.describe_snapshots( #for out particular volume finding respective latest snapshot
    OwnerIds=['self'],
    Filters = [
        {
            'Name': 'volume-id',
            'Values': [instance_volume['VolumeId']]
        },
    ]
)

latest_snapshot = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)
#print(latest_snapshot['StartTime']) #grabing latest snapshots

new_volume = ec2_client.create_volume( #now creating volume of with latest snapshot
    SnapshotId= latest_snapshot['SnapshotId'],
    AvailabilityZone= 'ap-south-1a', #hardcode this as well
    # our instance have a particular tag we want our new volume to have that tag also
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod' #tag this same as instance
                },
            ]
        },
    ],
)

#now we have to mount it when it is available
while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    if vol.state == 'availabe':
        ec2_resource.Instancd(instance_id).attach_volume(
            Device='/dev/xvdb',  # can't keep the same name change it from existing one
            VolumeId=new_volume['VolumeId']
        )
        break
