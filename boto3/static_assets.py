import os
import sys
import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "")


def main():
    bucket = sys.argv[1] if len(sys.argv) > 1 else "devops-projects-static-assets"
    path = sys.argv[2] if len(sys.argv) > 2 else "static/index.html"

    kw = {"region_name": REGION}
    if ENDPOINT:
        kw["endpoint_url"] = ENDPOINT
    s3 = boto3.client("s3", **kw)

    try:
        s3.create_bucket(Bucket=bucket)
        print(f"[+] bucket '{bucket}' created")
    except Exception as e:
        print(f"[=] bucket already exists ({e})")

    key = os.path.basename(path)
    with open(path, "rb") as f:
        s3.put_object(Bucket=bucket, Key=key, Body=f.read(), ContentType="text/html")
    print(f"[OK] uploaded {key}")

    for obj in s3.list_objects_v2(Bucket=bucket).get("Contents", []):
        print(f"    s3://{bucket}/{obj['Key']}  {obj['Size']} bytes")


if __name__ == "__main__":
    main()
