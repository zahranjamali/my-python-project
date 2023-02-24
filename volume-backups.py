import boto3
import schedule

ec2 = boto3.client('ec2')

def creating_snapshot():
    volumes = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'tag:environment',
                'Values': [
                    'prod',
                ]
            },
        ]
    )
    for volume in volumes['Volumes']:
        new_snapshot = ec2.client.create_snapshot(
            VolumeId=volume['VolumeId']
        )
        print(new_snapshot)

schedule.every().day.do(creating_snapshot)

while True:
    schedule.run_pending()