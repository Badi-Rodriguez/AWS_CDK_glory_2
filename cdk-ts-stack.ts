import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';

export class CdkTypescriptStack extends cdk.Stack {

    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        // ===== Generate a unique ID for the EC2 instance using the current date and time =====
        const idUnico = `ec2-instance-${new Date().toISOString().replace(/[-:.]/g, "")}`;

        // ===== Define a CloudFormation Parameter for the EC2 instance name =====
        const ec2Nombre = new cdk.CfnParameter(this, 'ec2-name', {
            type: 'String',
            default: 'MyInstance',
            description: 'Nombre de la instancia EC2'
        });

        // ===== Define a CloudFormation Parameter for the AMI (Ubuntu 22.04 LTS) =====
        const ami = new cdk.CfnParameter(this, 'ami', {
            type: 'String',
            default: 'ami-0aa28dab1f2852040', // Default AMI for Ubuntu 22.04
            description: 'AMI de Ubuntu Server 22.04 LTS'
        });

        // ===== Use an existing IAM Role called 'LabRole' to grant permissions to the EC2 instance =====
        const role = iam.Role.fromRoleArn(this, 'LabRole', `arn:aws:iam::${this.account}:role/LabRole`);

        // ===== Look up the default VPC in the account =====
        const vpc = ec2.Vpc.fromLookup(this, 'Vpc', { isDefault: true });

        // ===== Create a Security Group to allow SSH (port 22) and HTTP (port 80) traffic =====
        const securityGroup = new ec2.SecurityGroup(this, 'SecurityGroup', {
            vpc,
            description: 'Allow SSH and HTTP traffic',
            allowAllOutbound: true  // Allow all outgoing traffic from the instance
        });

        // ===== Add rules to allow inbound SSH (port 22) and HTTP (port 80) traffic =====
        securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'Allow SSH access'); // Allow SSH
        securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'Allow HTTP access'); // Allow HTTP

        // ===== Define the User Data to execute when the instance starts =====
        // The script will clone two GitHub repositories into the web server directory
        const userData = ec2.UserData.forLinux();
        userData.addCommands(
            "#!/bin/bash",  // Shell script to be executed
            "cd /var/www/html",  // Change to the web server root directory
            "git clone https://github.com/utec-cc-2024-2-test/websimple.git",  // Clone the 'websimple' project
            "git clone https://github.com/utec-cc-2024-2-test/webplantilla.git",  // Clone the 'webplantilla' project
            "ls -l"  // List the files to verify successful cloning
        );

        // ===== Create the EC2 instance =====
        const instance = new ec2.Instance(this, idUnico, {
            instanceType: new ec2.InstanceType('t2.micro'),  // Use t2.micro instance (part of the AWS free tier)
            machineImage: ec2.MachineImage.genericLinux({ 'us-east-1': ami.valueAsString }),  // Use the specified Ubuntu AMI
            vpc,  // Deploy the instance in the default VPC
            securityGroup,  // Attach the security group to the instance
            role,  // Attach the IAM role
            keyName: 'vockey',  // Use the existing key pair for SSH access
            blockDevices: [{
                deviceName: '/dev/sda1',  // Define the root EBS volume device name
                volume: ec2.BlockDeviceVolume.ebs(20),  // Attach a 20GB EBS volume
            }],
            userData  // Run the User Data script upon instance initialization
        });

        // ===== Add a 'Name' tag to the EC2 instance =====
        cdk.Tags.of(instance).add('Name', ec2Nombre.valueAsString);

        // ===== CloudFormation Outputs =====
        // Output the instance ID, public IP address, and URLs for the web projects
        new cdk.CfnOutput(this, 'InstanceID', { value: instance.instanceId });
        new cdk.CfnOutput(this, 'PublicIP', { value: instance.instancePublicIp });
        new cdk.CfnOutput(this, 'WebSimpleURL', { value: `http://${instance.instancePublicIp}/websimple` });
        new cdk.CfnOutput(this, 'WebPlantillaURL', { value: `http://${instance.instancePublicIp}/webplantilla` });
    }
}
