from aws_cdk import (
    Stack,
    aws_ec2 as ec2,  # Import EC2 module for creating instances
    aws_iam as iam,  # Import IAM for role management
    CfnParameter,  # Import to create CloudFormation parameters
    CfnOutput,  # Import to create CloudFormation outputs
    Tags  # Import to add tags to AWS resources
)
from constructs import Construct
from datetime import datetime  # Import to generate unique IDs based on the current date and time

class PilaEc2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:

        # Generate a unique ID for the EC2 instance using the current date and time
        id_unico = f"ec2-instancia-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        super().__init__(scope, id_unico, **kwargs)

        # Define a CloudFormation parameter to specify the EC2 instance name
        ec2Nombre = CfnParameter(self, "ec2-nombre", type="String", default="MV Default",
                                 description="Nombre de la instancia")

        # Define a CloudFormation parameter for the Amazon Machine Image (AMI) of Ubuntu 22.04 LTS
        ami = CfnParameter(self, "ami", type="String", default="ami-0aa28dab1f2852040",
                           description="Ubuntu Server 22.04 LTS")

        # Use an existing IAM Role called 'LabRole' to give the instance permissions to perform AWS actions
        rol = iam.Role.from_role_arn(self, "rol", role_arn=f"arn:aws:iam::{self.account}:role/LabRole")

        # Look up and use the default VPC (Virtual Private Cloud) in the AWS account
        nube = ec2.Vpc.from_lookup(self, "vpc", is_default=True)

        # Create a security group to allow SSH (port 22) and HTTP (port 80) traffic to the EC2 instance
        grupoSeguridad = ec2.SecurityGroup(
            self, "grupo-seguridad-ec2",
            vpc=nube,  # Attach the security group to the VPC
            description="Permitir tráfico SSH y HTTP desde 0.0.0.0/0",  # Allow traffic from any IP
            allow_all_outbound=True  # Allow all outgoing traffic from the instance
        )

        # Allow inbound SSH traffic on port 22 from any IP address
        grupoSeguridad.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Permitir SSH"
        )

        # Allow inbound HTTP traffic on port 80 from any IP address
        grupoSeguridad.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Permitir HTTP"
        )

        # Define the User Data script to be executed when the instance is created
        # This script clones two GitHub repositories (websimple and webplantilla)
        datosUsuario = ec2.UserData.for_linux()
        datosUsuario.add_commands(
            "#!/bin/bash",  # Bash script to run on instance initialization
            "cd /var/www/html/",  # Change directory to the web server root
            "git clone https://github.com/utec-cc-2024-2-test/websimple.git",  # Clone websimple project
            "git clone https://github.com/utec-cc-2024-2-test/webplantilla.git",  # Clone webplantilla project
            "ls -l"  # List files in the directory to verify successful cloning
        )

        # Create the EC2 instance with the specified configuration
        ec2Instancia = ec2.Instance(
            self, id_unico,  # Use the unique ID generated earlier
            instance_type=ec2.InstanceType("t2.micro"),  # Define the instance type (t2.micro is part of the free tier)
            machine_image=ec2.MachineImage.generic_linux({"us-east-1": ami.value_as_string}),  # Use the AMI for Ubuntu 22.04
            vpc=nube,  # Deploy the instance in the default VPC
            security_group=grupoSeguridad,  # Attach the security group created earlier
            key_pair=ec2.KeyPair.from_key_pair_name(self, "keyPair", "vockey"),  # Use an existing SSH key pair for access
            role=rol,  # Attach the IAM role for permissions
            block_devices=[ec2.BlockDevice(  # Define the root EBS volume for the instance
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)  # Create a 20GB EBS volume
            )],
            user_data=datosUsuario  # Run the User Data script when the instance is initialized
        )

        # Add a tag to the EC2 instance to identify it by name
        Tags.of(ec2Instancia).add('Name', ec2Nombre.value_as_string)

        # CloudFormation outputs to display the instance ID and public IP address
        CfnOutput(self, "ID", value=ec2Instancia.instance_id)
        CfnOutput(self, "IP Publica", value=ec2Instancia.instance_public_ip)
        # Output URLs to access the web projects cloned from GitHub
        CfnOutput(self, "websimpleURL", value=f"http://{ec2Instancia.instance_public_ip}/websimple")
        CfnOutput(self, "webplantillaURL", value=f"http://{ec2Instancia.instance_public_ip}/webplantilla")
