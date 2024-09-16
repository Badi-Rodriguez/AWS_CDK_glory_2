mkdir cloud9-instance
cd cloud9-instance
cdk init app --language python

python -m pip install aws-cdk-lib aws-cdk.aws-ec2 aws-cdk.aws-iam
