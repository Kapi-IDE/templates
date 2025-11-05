# Comprehensive AWS Infrastructure Template

This template provides a complete AWS infrastructure setup using Infrastructure as Code (IaC) best practices, incorporating the latest AWS services and tools available in 2025.

## Overview

This template leverages AWS CDK, Terraform, and CloudFormation in a hybrid approach to provide flexibility and comprehensive coverage of AWS services. It's designed for production-grade applications with high availability, security, and scalability requirements.

## 1. Project Structure

```bash
aws-infrastructure/
├── cdk/                      # AWS CDK components
│   ├── bin/
│   ├── lib/
│   │   ├── networking/
│   │   ├── compute/
│   │   ├── database/
│   │   ├── security/
│   │   └── monitoring/
│   ├── test/
│   └── cdk.json
├── terraform/                # Terraform modules
│   ├── modules/
│   │   ├── vpc/
│   │   ├── eks/
│   │   ├── rds/
│   │   └── s3/
│   ├── environments/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── main.tf
├── cloudformation/           # CloudFormation templates
│   ├── templates/
│   │   ├── networking/
│   │   └── iam/
│   └── parameters/
├── scripts/                  # Deployment scripts
│   ├── deploy.sh
│   ├── rollback.sh
│   └── validate.sh
├── docs/                     # Documentation
│   ├── architecture.md
│   ├── deployment.md
│   └── troubleshooting.md
└── config/                   # Configuration files
    ├── environments.json
    └── security-groups.json
```

## 2. AWS CDK Setup (TypeScript)

### 2.1 Initialize CDK Project

```bash
# Install CDK CLI
npm install -g aws-cdk

# Initialize CDK project
mkdir cdk && cd cdk
cdk init app --language typescript

# Install dependencies
npm install @aws-cdk/aws-ec2 @aws-cdk/aws-ecs @aws-cdk/aws-rds @aws-cdk/aws-s3 @aws-cdk/aws-cloudfront @aws-cdk/aws-lambda @aws-cdk/aws-apigateway
```

### 2.2 VPC Stack (cdk/lib/networking/vpc-stack.ts)

```typescript
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

export class VpcStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.vpc = new ec2.Vpc(this, 'MainVpc', {
      maxAzs: 3,
      natGateways: 2,
      subnetConfiguration: [
        {
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
        {
          name: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
          cidrMask: 24,
        },
        {
          name: 'Isolated',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
          cidrMask: 24,
        },
      ],
      flowLogs: {
        s3: {
          destination: ec2.FlowLogDestination.toS3(),
          trafficType: ec2.FlowLogTrafficType.ALL,
        },
      },
    });

    // Add VPC endpoints for AWS services
    this.vpc.addGatewayEndpoint('S3Endpoint', {
      service: ec2.GatewayVpcEndpointAwsService.S3,
    });

    this.vpc.addInterfaceEndpoint('SecretsManagerEndpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
    });
  }
}
```

### 2.3 ECS Fargate Stack (cdk/lib/compute/ecs-stack.ts)

```typescript
import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as elb from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import { Construct } from 'constructs';

export interface EcsStackProps extends cdk.StackProps {
  vpc: ec2.Vpc;
}

export class EcsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: EcsStackProps) {
    super(scope, id, props);

    const cluster = new ecs.Cluster(this, 'Cluster', {
      vpc: props.vpc,
      containerInsights: true,
    });

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef', {
      memoryLimitMiB: 512,
      cpu: 256,
    });

    const container = taskDefinition.addContainer('AppContainer', {
      image: ecs.ContainerImage.fromRegistry('nginx:latest'),
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'app' }),
      environment: {
        NODE_ENV: 'production',
      },
    });

    container.addPortMappings({
      containerPort: 80,
    });

    const service = new ecs.FargateService(this, 'Service', {
      cluster,
      taskDefinition,
      desiredCount: 2,
      assignPublicIp: false,
    });

    const lb = new elb.ApplicationLoadBalancer(this, 'ALB', {
      vpc: props.vpc,
      internetFacing: true,
    });

    const listener = lb.addListener('Listener', {
      port: 80,
      open: true,
    });

    listener.addTargets('ECS', {
      port: 80,
      targets: [service],
      healthCheck: {
        path: '/health',
        interval: cdk.Duration.seconds(30),
      },
    });
  }
}
```

## 3. Terraform Modules

### 3.1 VPC Module (terraform/modules/vpc/main.tf)

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.availability_zones[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.environment}-public-${count.index + 1}"
    Environment = var.environment
    Tier        = "Public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 100)
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name        = "${var.environment}-private-${count.index + 1}"
    Environment = var.environment
    Tier        = "Private"
  }
}
```

### 3.2 EKS Cluster Module (terraform/modules/eks/main.tf)

```hcl
resource "aws_eks_cluster" "main" {
  name     = "${var.environment}-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
    security_group_ids      = [aws_security_group.eks_cluster.id]
  }

  encryption_config {
    provider {
      key_arn = var.kms_key_arn
    }
    resources = ["secrets"]
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
    aws_iam_role_policy_attachment.eks_service_policy,
  ]
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.environment}-node-group"
  node_role_arn   = aws_iam_role.eks_node.arn
  subnet_ids      = var.private_subnet_ids

  scaling_config {
    desired_size = var.desired_capacity
    max_size     = var.max_capacity
    min_size     = var.min_capacity
  }

  instance_types = var.instance_types

  tags = {
    Environment = var.environment
  }
}
```

## 4. CloudFormation Templates

### 4.1 IAM Roles (cloudformation/templates/iam/roles.yaml)

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: IAM roles for application services

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]

Resources:
  EC2Role:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub ${Environment}-ec2-role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
        - arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy

  ECSTaskExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub ${Environment}-ecs-task-execution-role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

## 5. Security and Compliance

### 5.1 Security Groups Configuration

```typescript
// cdk/lib/security/security-groups.ts
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

export class SecurityGroups extends Construct {
  public readonly webTierSg: ec2.SecurityGroup;
  public readonly appTierSg: ec2.SecurityGroup;
  public readonly dbTierSg: ec2.SecurityGroup;

  constructor(scope: Construct, id: string, vpc: ec2.Vpc) {
    super(scope, id);

    // Web tier security group
    this.webTierSg = new ec2.SecurityGroup(this, 'WebTierSG', {
      vpc,
      description: 'Security group for web tier',
      allowAllOutbound: true,
    });

    this.webTierSg.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(443),
      'Allow HTTPS traffic'
    );

    // Application tier security group
    this.appTierSg = new ec2.SecurityGroup(this, 'AppTierSG', {
      vpc,
      description: 'Security group for application tier',
      allowAllOutbound: true,
    });

    this.appTierSg.addIngressRule(
      this.webTierSg,
      ec2.Port.tcp(8080),
      'Allow traffic from web tier'
    );

    // Database tier security group
    this.dbTierSg = new ec2.SecurityGroup(this, 'DbTierSG', {
      vpc,
      description: 'Security group for database tier',
      allowAllOutbound: false,
    });

    this.dbTierSg.addIngressRule(
      this.appTierSg,
      ec2.Port.tcp(5432),
      'Allow PostgreSQL from app tier'
    );
  }
}
```

## 6. Monitoring and Logging

### 6.1 CloudWatch Dashboard

```typescript
// cdk/lib/monitoring/dashboard.ts
import * as cdk from 'aws-cdk-lib';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import { Construct } from 'constructs';

export class MonitoringDashboard extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    const dashboard = new cloudwatch.Dashboard(this, 'AppDashboard', {
      dashboardName: 'ApplicationMonitoring',
    });

    // Add widgets for key metrics
    dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'EC2 CPU Utilization',
        left: [/* metrics */],
      }),
      new cloudwatch.GraphWidget({
        title: 'ALB Request Count',
        left: [/* metrics */],
      }),
      new cloudwatch.GraphWidget({
        title: 'RDS Database Connections',
        left: [/* metrics */],
      })
    );
  }
}
```

## 7. Deployment Scripts

### 7.1 Main Deployment Script (scripts/deploy.sh)

```bash
#!/bin/bash
set -e

ENVIRONMENT=$1
if [ -z "$ENVIRONMENT" ]; then
    echo "Usage: ./deploy.sh <environment>"
    exit 1
fi

echo "Deploying infrastructure for environment: $ENVIRONMENT"

# Deploy CDK stacks
cd cdk
cdk deploy --all --require-approval never

# Deploy Terraform modules
cd ../terraform/environments/$ENVIRONMENT
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# Deploy CloudFormation templates
aws cloudformation deploy \
    --template-file ../../cloudformation/templates/iam/roles.yaml \
    --stack-name $ENVIRONMENT-iam-roles \
    --parameter-overrides Environment=$ENVIRONMENT \
    --capabilities CAPABILITY_NAMED_IAM

echo "Deployment completed successfully"
```

## 8. Best Practices Summary

1. **Multi-Tool Approach**: Use CDK for complex infrastructure, Terraform for cross-cloud resources, and CloudFormation for IAM and security policies
2. **Environment Separation**: Maintain separate configurations for dev, staging, and production
3. **Security First**: Implement least privilege access, encryption at rest and in transit
4. **Monitoring**: Comprehensive logging and monitoring with CloudWatch
5. **Cost Optimization**: Use auto-scaling, spot instances, and reserved instances where appropriate
6. **Compliance**: Ensure all resources are tagged and meet compliance requirements
7. **Documentation**: Maintain comprehensive documentation for all infrastructure components

## 9. Getting Started

```bash
# Prerequisites
- AWS CLI configured with appropriate credentials
- Node.js 18+ installed
- Terraform 1.5+ installed
- CDK CLI installed

# Clone the repository
git clone <repository-url>
cd aws-infrastructure

# Deploy development environment
./scripts/deploy.sh dev

# Deploy staging environment
./scripts/deploy.sh staging

# Deploy production environment
./scripts/deploy.sh prod
```

This template provides a comprehensive AWS infrastructure setup that can be customized for specific project needs while following AWS best practices and modern IaC approaches.
