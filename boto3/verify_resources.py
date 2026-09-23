import os
import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "")


def client(service):
    kw = {"region_name": REGION}
    if ENDPOINT:
        kw["endpoint_url"] = ENDPOINT
    return boto3.client(service, **kw)


def main():
    print("== EC2 instances ==")
    try:
        resp = client("ec2").describe_instances()
        count = 0
        for r in resp["Reservations"]:
            for i in r["Instances"]:
                count += 1
                print(f"  {i['InstanceId']}  {i['State']['Name']:<10} {i['InstanceType']}")
        if count == 0:
            print("  (none)")
    except Exception as e:
        print("  [error]", e)

    print("== Security groups ==")
    try:
        for sg in client("ec2").describe_security_groups()["SecurityGroups"]:
            print(f"  {sg['GroupName']:<12} inbound_rules={len(sg['IpPermissions'])}")
    except Exception as e:
        print("  [error]", e)

    print("== S3 buckets ==")
    try:
        for b in client("s3").list_buckets()["Buckets"]:
            print(f"  {b['Name']}  created={b['CreationDate']}")
    except Exception as e:
        print("  [error]", e)


if __name__ == "__main__":
    main()
