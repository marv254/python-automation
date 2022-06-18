import boto3
from operator import itemgetter
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

instance_id = 'i-06e2b2f422dfccbf4'

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        },
    ],
)
instance_volume = volumes['Volumes'][0]
# print(instance_volume)

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
            {
                'Name': 'volume-id',
                'Values': [instance_volume['VolumeId']]
            }
        ]
)
latest_snapshots = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)[0]

print(latest_snapshots['StartTime'])

new_volume = ec2_client.create_volume(
    SnapshotId=latest_snapshots['SnapshotId'],
    AvailabilityZone='af-south-1c',
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                }
            ]
        }
    ]
)

while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    print(vol.state)
    if vol.state == 'available':
        ec2_resource.Instance(instance_id).attach_volume(
            VolumeId=new_volume['VolumeId'],
            Device='/dev/xvdb'
        )
        break