import json
import boto3

client=boto3.client('emr', region_name='ap-southeast-2')


def lambda_handler(event, context):
    response=client.run_job_flow(
        Name='commerce',
        LogUri='s3://e-commerce-yiding/emr-logs/',
        ReleaseLabel='emr-6.3.0',
        Instances={
            #'MasterInstanceType': 'm4.large',
            #'SlaveInstanceType': 'm4.large',
            'InstanceGroups': [
                {
                    'Name': "Master nodes",
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'MASTER',
                    'InstanceType': 'm4.large',
                    'InstanceCount': 1,
                },
                {
                    'Name': "Slave nodes",
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'CORE',
                    'InstanceType': 'm4.large',
                    'InstanceCount': 2,
                }
            ],
            'Ec2KeyName': 'ap-southeast-2-keypair',
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False,
            'Ec2SubnetId': 'subnet-05f749b3375e34850',
        },
        Applications=[
            {
                'Name':'Hadoop'
                #'Version':'3.2.1'
            },
            {
                'Name':'Spark'
                #'Version':'3.1.1'
            },
            {
                'Name':'Hive'
                #'Version':'3.1.2'
            },
            {
                'Name':'Zeppelin'
                #'Version':'0.9.0'
            },
            {
                'Name':'Hue'
                #'Version':'4.9.0'
            },
            {
                'Name':'Sqoop'
            }
        ],
        VisibleToAllUsers=True,
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole',
        EbsRootVolumeSize=15
    )