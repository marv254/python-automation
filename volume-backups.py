import boto3

ec2_client = boto3.client('ec2')

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['prod']
        }
    ]
)

for volume in volumes['Volumes']:
    new_snapshot = ec2_client.create_snapshot(
        VolumeId=volume['VolumeId']
    )
    print(new_snapshot)

