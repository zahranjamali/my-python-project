import boto3

ec2_client_mumbai = boto3.client('ec2')
ec2_resource_mumbai = boto3.resource('ec2')


instance_id_mumbai = []

reservations_mumbai = ec2_client_mumbai.describe_instances()["Reservations"]
for reservation in reservations_mumbai:
    instances = reservation["Instances"]
    for inst in instances:
        instance_id_mumbai.append(inst["InstanceId"])
print(instance_id_mumbai)

response = ec2_resource_mumbai.create_tags(
    Resources=instance_id_mumbai,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'pod'
        },
    ]
)
print("successfully added tags")
