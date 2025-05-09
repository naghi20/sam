#!/bin/sh

sam deploy \
  --template-file ./template.yaml \
  --stack-name order-processing-stack \
  --capabilities CAPABILITY_IAM \
  --region eu-west-2 \
  --resolve-s3 \
  --no-fail-on-empty-changeset \
  2>&1 | tee sam_deploy_output.log

# Description of options ...
# --template-file: Path to your SAM template.
# --stack-name: CloudFormation stack name to create/update.
# --capabilities CAPABILITY_IAM: Required to create IAM roles/policies.
# --region: AWS region for deployment.
# --resolve-s3: Automatically creates & manages S3 bucket for code packaging.
# --no-fail-on-empty-changeset: Prevents failure if there are no changes.

