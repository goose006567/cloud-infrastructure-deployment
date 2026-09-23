# Project 2: Automated Cloud Infrastructure Deployment (AWS · Terraform · Boto3)

A three-tier AWS architecture provisioned **100% as code** — and the whole lifecycle runs **offline** against a local mock AWS (moto), so nothing is billed and no real credentials are needed.

## What it deploys

```
                        Internet
                           |
                      [devops-alb]  SG 80/443 from 0.0.0.0/0
                           |
Public subnet 10.0.1.0/24  [web-01]      SG devops-web (80 only from ALB)  + EIP/NAT in public subnet
                           |  <- NAT gateway for outbound updates
Private app  10.0.2.0/24   [app-01]      SG devops-app (8080 only from web)
                           |
Private db   10.0.3.0/24   [db-01]       SG devops-db  (3306 only from app)

S3 bucket (private)  <- OAC ->  CloudFront distribution (static asset delivery)
```

- **Least-privilege security groups** are chained: each tier only accepts traffic from the tier in front of it (ALB → web → app → db).
- **S3 + CloudFront**: bucket is private; CloudFront accesses it via Origin Access Control (OAC) — the asset-delivery use case.
- 26 resources total in `terraform/`.

## Project layout

```
terraform/
├── version.tf          # terraform + provider pins
├── providers.tf        # region, offline flags, optional moto endpoint
├── variables.tf
├── networking.tf       # VPC, 3 subnets, IGW, NAT+EIP, route tables
├── security_groups.tf  # chained least-privilege
├── compute.tf          # web / app / db instances
├── s3_cloudfront.tf    # private bucket + OAC + CloudFront distribution
└── outputs.tf
boto3/
├── verify_resources.py # list EC2 / SGs / S3 (validates what terraform built)
├── static_assets.py    # upload a static asset to S3
└── static/index.html
mock_aws.py             # moto server: offline AWS API (ec2, s3, cloudfront, sts)
```

## How it was verified — fully offline

```bash
cd terraform
terraform init                                     # downloads AWS provider once
terraform fmt -check && terraform validate         # syntax + schema validation
AWS_ACCESS_KEY_ID=dummy AWS_SECRET_ACCESS_KEY=dummy terraform plan   # no creds needed

# full deploy against the offline moto mock (AirPlay owns :5000 on macOS, so use 4566)
python3.12 -m venv .venv && .venv/bin/pip install boto3 "moto[server]>=5"
MOTO_PORT=4566 .venv/bin/python mock_aws.py &
AWS_ACCESS_KEY_ID=dummy AWS_SECRET_ACCESS_KEY=dummy \
AWS_DEFAULT_REGION=us-east-1 \
terraform apply -auto-approve -var mock_endpoint=http://127.0.0.1:4566
# -> Apply complete! Resources: 26 added

# prove it with boto3
export AWS_ACCESS_KEY_ID=dummy AWS_SECRET_ACCESS_KEY=dummy \
       AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=http://127.0.0.1:4566
.venv/bin/python boto3/verify_resources.py
.venv/bin/python boto3/static_assets.py devops-projects-static-assets boto3/static/index.html
```

## Going to real AWS (after this project)

1. `aws configure` with real credentials.
2. Remove `skip_credentials_validation` / `skip_requesting_account_id` in `providers.tf`.
3. Replace the hardcoded `ami` in `variables.tf` (region-specific), set `bucket_name` to a globally unique name.
4. `terraform apply` — nothing else changes; the same code deploys the real stack.

## Things learned

- `terraform fmt` normalizes code; `terraform validate` catches **schema** errors *before* any cloud call — don't skip them.
- AWS policy: security group names **cannot start with `sg-`** (reserved prefix) — validation caught it.
- Terraform AWS provider (v5) calls `STS GetCallerIdentity` even to plan; `skip_credentials_validation` + `skip_requesting_account_id` keep plan/apply offline.
- macOS **AirPlay Receiver occupies port 5000** — an easy trap when picking a mock port.
- `data "aws_iam_policy_document"` renders locally (no API call) — great for offline policy work.
- moto gives us the full IaC lifecycle: `init → validate → plan → apply → destroy` without touching AWS.

## Résumé-ready summary

> Designed a three-tier AWS architecture with public/private VPC subnets and security groups following least-privilege access principles. Provisioned all infrastructure as code with Terraform for repeatable, version-controlled deployments. Automated resource management and validation with Python/Boto3. Integrated S3 and CloudFront for static asset delivery.
