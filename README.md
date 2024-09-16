# AWS_CDK_glory_2
I use this repository to work on the second part of our project for Cloud Computing at college UTEC.

# README - AWS EC2 Instance Setup using AWS CDK

## Introduction

This guide walks you through setting up an **AWS EC2 instance** using the **AWS Cloud Development Kit (CDK)**. AWS CDK allows you to define cloud infrastructure in code using modern programming languages (TypeScript, Python, Java, .NET, etc.) and deploy it through AWS CloudFormation.

This specific setup mimics the environment you'd get from **AWS Cloud9**—an EC2-based development environment commonly used for coding, development, and system administration.

### What is AWS CDK?

The **AWS Cloud Development Kit (CDK)** is a software framework that allows you to define your AWS cloud infrastructure as code and deploy it using AWS CloudFormation. CDK lets you use familiar programming languages such as **TypeScript**, **Python**, **Java**, and **.NET** to model and provision AWS resources.

### What Can You Do with AWS CDK?

- **Define cloud resources** like EC2, S3, Lambda, VPCs, etc., using code.
- **Deploy cloud resources** with AWS CloudFormation via CDK CLI.
- **Manage resources** by checking differences between deployed and new configurations, updating, or deleting stacks.
- **Use AWS Construct Hub** for pre-built components to accelerate infrastructure design.

For more information on AWS CDK, visit:  
<https://aws.amazon.com/cdk/>

---

## Project Overview

This project creates an AWS EC2 instance using the **Python** language in AWS CDK, and configures the instance with **Node.js**, **AWS CDK**, and other developer tools commonly found in AWS Cloud9.

### Features

- **EC2 Instance**: A t3.micro (or other instance types) running Amazon Linux 2 or Ubuntu.
- **Security Group**: Allows SSH (port 22) and HTTP (port 80) access.
- **IAM Role**: Allows EC2 access to AWS Systems Manager (SSM), enabling remote management without SSH.
- **User Data**: Configures the EC2 instance with Python, Node.js, AWS CDK, and other developer tools.

---

## Prerequisites

### Tools

1. **AWS CLI**  
   Install the AWS Command Line Interface (CLI) for managing AWS services.  
   Guide: <https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html>

2. **Node.js and npm**  
   Install Node.js, which is required for AWS CDK and many modern development environments.  
   Guide: <https://nodejs.org/en/download/>

3. **AWS CDK CLI**  
   Install the AWS CDK Command Line Interface (CLI) to interact with the AWS CDK application.  
   Command:
   ```bash
   npm install -g aws-cdk
4. **Python**
   Install python for development and to manage virtual enviorments related to the instance and image. (Here: https://www.python.org/downloads/)

## Details

**AWS Cloud9 and EC2 Setup:**
AWS Cloud9 is a development environment that automatically configures instances with tools like Node.js, Python, and more. In this project, we replicate a basic setup using an EC2 instance with user data scripts to automatically install and configure developer tools.
- **Security group:** We use Vockey for simplicity's sake as access through SSH and HTTP.
- **IAM ROLE:** Attaches an IAM role with SSM permissions to allow management without SSH.

## Instructions

(All commands ennacted on the ICL)
1. **Install AWS CDK and Initialize the Project** : Start by creating a directory for your project and initializing it as a CDK app using Python. (Associated file named: assembler)
2. **Install Required Libraries** : Execute following line of code: `python -m pip install aws-cdk-lib aws-cdk.aws-ec2 aws-cdk.aws-iam`
3. **Define the EC2 Instance in Stack** : Perform the process within the file proccess_run.py
4. **Stack deployment** : (First verify existance with: `cdk bootstrap`) Execute line: `cdk deploy` (Set public IP address, IPv4)
5. **Verify access point**: Execute line on AWS command line for session: `$ ssh -i /path/to/key.pem ec2-user@<INSTANCE_PUBLIC_IP>`.

## Setup and Deployment

This section outlines the steps to install, configure, and deploy the infrastructure using AWS CDK.

1. **Install AWS CDK and Initialize the Project**  
   Start by creating a directory for your project and initializing it as a CDK app using Python.
   ```bash
   mkdir aws-cdk-project
   cd aws-cdk-project
   cdk init app --language python
2. **Install required libraries**
   Install the necessary libraries for AWS CDK, EC2, and IAM by running the following:
   `python -m pip install aws-cdk-lib aws-cdk.aws-ec2 aws-cdk.aws-iam`
3. **Define the EC2 instance**
   Define the EC2 instance in your stack by editing the app_sys.py and final_app.py file. This will include setting up the instance type, security groups, and user data. Finally very the contents of CDK-typescript.ts and CDK-ts-typescript.ts for the generation.
4. **Deploy the Stack**
   Make sure the enviormeny is bootstrapped with `cdk bootstrap`.
   Then deploy with `cdk deploy`
   Finally, verify access through ssh entry with: `ssh -i /path/to/key.pem ec2-user@<INSTANCE_PUBLIC_IP>`

## References
- AWS CDK Documentation: https://docs.aws.amazon.com/cdk/latest/guide/home.html
- AWS EC2 User Guide: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html
- AWS Cloud9: https://aws.amazon.com/cloud9/
- IAM Roles in AWS: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html
