#!/usr/bin/env python3
import boto3, sys, os, datetime

def log_to_cloudwatch(logfile, log_group):
    region = os.getenv("AWS_DEFAULT_REGION", "eu-west-2")
    logs = boto3.client("logs", region_name=region)
    log_stream = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    try:
        logs.create_log_group(logGroupName=log_group)
    except logs.exceptions.ResourceAlreadyExistsException:
        pass
    try:
        logs.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
    except logs.exceptions.ResourceAlreadyExistsException:
        pass

    with open(logfile, "r") as f:
        content = f.read()

    logs.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{
            "timestamp": int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000),
            "message": content[:10000],
        }],
    )
    print(f"✅ Logged {logfile} to CloudWatch group: {log_group}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: log_to_cloudwatch.py <file> <log_group>")
        sys.exit(1)
    log_to_cloudwatch(sys.argv[1], sys.argv[2])