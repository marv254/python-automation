import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

reservations = ec2_client.describe_instances()

# for reservation in reservations["Reservations"]:
#     instances = reservation["Instances"]
#
#     for instance in instances:
#         print(f"Instance {instance['InstanceId']} is {instance['State']['Name']}")

statuses = ec2_client.describe_instance_status()

for status in statuses["InstanceStatuses"]:
    ins_status = status["InstanceStatus"] ["Status"]
    sys_status = status["SystemStatus"]["Status"]
    state = status["InstanceState"]["Name"]
    print(f"Instance {status['InstanceId']} is {state} status is {ins_status} and system status is {sys_status}")
