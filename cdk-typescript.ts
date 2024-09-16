import * as cdk from 'aws-cdk-lib';  // Import the core AWS CDK library

import { CdkTypescriptStack } from '../lib/cdk-typescript-stack';  // Import the custom stack definition

import { STSClient, GetCallerIdentityCommand } from '@aws-sdk/client-sts';  // Import STS client to get AWS account information

// Main function to set up and deploy the CDK stack
async function main() {
    const app = new cdk.App();  // Create a new CDK application

    // Create an STS client to retrieve AWS account information
    const stsClient = new STSClient({ region: process.env.AWS_REGION || 'us-east-1' });  // Use the specified AWS region or default to 'us-east-1'

    // Use the STS client to get the current Account ID
    const data = await stsClient.send(new GetCallerIdentityCommand({}));

    // Extract the AWS Account ID from the response
    const accountId = data.Account!;  // AWS Account ID
    const region = process.env.AWS_REGION || 'us-east-1';  // Use the specified AWS region or default to 'us-east-1'

    // Define a new qualifier that will be used to uniquely name resources
    const qualifier = 'ec2-dep';  // 'ec2-dep' is the chosen qualifier for this deployment

    // Define the AWS environment using the retrieved Account ID and region
    const env = { account: accountId, region: region };  // Environment contains the AWS account and region for deployment

    // Configure the synthesizer, which controls how assets and resources are deployed
    const synthesizer = new cdk.DefaultStackSynthesizer({
        qualifier: qualifier,  // A unique qualifier to avoid naming collisions
        cloudFormationExecutionRole: `arn:aws:iam::${accountId}:role/LabRole`,  // Use the IAM role 'LabRole' for CloudFormation execution
        fileAssetsBucketName: `cdk-${qualifier}-assets-${accountId}-${region}`,  // Define the S3 bucket for storing deployment assets
    });

    // Create and deploy the stack, passing in the environment and synthesizer
    new CdkTypescriptStack(app, 'PilaEc2', { env, synthesizer });

    // Synthesize the CDK application, preparing it for deployment
    app.synth();
}

// Run the main function to execute the deployment
main();
