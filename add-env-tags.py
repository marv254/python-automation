import boto3

ec2_client_africa = boto3.client('ec2')
ec2_resource_africa = boto3.resource('ec2')

instance_ids_africa = []

reservations_africa = ec2_client_africa.describe_instances()['Reservations']

for reservation in reservations_africa:
    instances = reservation['Instances']
    for instance in instances:
        instance_ids_africa.append(instance['InstanceId'])


response = ec2_resource_africa.create_tags(
    Resources=instance_ids_africa,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)
