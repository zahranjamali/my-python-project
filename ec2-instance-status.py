import boto3
import schedule

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

def Instance_status():
    reservations = ec2_client.describe_instances(
    )
    for reservation in reservations["Reservations"]:
        instances = reservation["Instances"]
        for instance in instances:
            print(f"for instance {instance['InstanceId']}  is {instance['State']['Name']}")
    instance_status = ec2_client.describe_instance_status()
    for inst in instance_status["InstanceStatuses"]:
        inst_status = inst["InstanceStatus"]["Status"]
        sys_status = inst["SystemStatus"]["Status"]
        state = inst["InstanceState"]
        print(f"for instance {inst['InstanceId']}is {state} status is {inst_status}system is {sys_status}")

schedule.every(5).seconds.do(Instance_status)

while True:
    schedule.run_pending()
