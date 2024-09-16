from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core  # CDK v1 used aws_cdk.core, CDK v2 uses aws-cdk-lib
)

class Cloud9InstanceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Step 1: Create a VPC (Virtual Private Cloud)
        vpc = ec2.Vpc(self, "Cloud9Vpc",
            max_azs=2,  # Deploy the instance in two availability zones for high availability
            nat_gateways=1
        )

        # Step 2: Create a Security Group for the EC2 Instance
        security_group = ec2.SecurityGroup(self, "Cloud9SG",
            vpc=vpc,
            description="Allow SSH and HTTP access to EC2 instance",
            allow_all_outbound=True
        )

        # Allow SSH (port 22) from anywhere (0.0.0.0/0). You should restrict this to your IP for security.
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow SSH access from anywhere"
        )

        # Allow HTTP access (port 80)
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP access from anywhere"
        )

        # Step 3: Define the EC2 Instance Role (with SSM permissions, which Cloud9 uses)
        role = iam.Role(self, "Cloud9InstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        # Attach SSM (System Manager) permissions to the EC2 instance role (for remote management)
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Step 4: Launch an EC2 instance (Ubuntu-based AMI)
        ec2_instance = ec2.Instance(self, "Cloud9Instance",
            instance_type=ec2.InstanceType("t3.micro"),  # Choose the instance type (t3.micro is free-tier eligible)
            machine_image=ec2.MachineImage.latest_amazon_linux(),  # Use Amazon Linux 2 AMI (or Ubuntu)
            vpc=vpc,
            security_group=security_group,
            role=role,
            key_name="my-key-pair"  # Optional: Your SSH key for EC2 access
        )

        # Step 5: (Optional) User data script to configure the EC2 instance (e.g., install Python, CDK, and Cloud9-like tools)
        ec2_instance.add_user_data(
            "#!/bin/bash",
            "sudo apt-get update -y",
            "sudo apt-get install -y python3 python3-pip",
            "curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -",
            "sudo apt-get install -y nodejs",
            "sudo npm install -g aws-cdk",  # Install AWS CDK
            "sudo apt-get install -y vim git"  # Optional: Developer tools
        )

        # Output the public IP address of the instance
        core.CfnOutput(self, "InstancePublicIP", value=ec2_instance.instance_public_ip)
