#!/usr/bin/env python3
import boto3, sys, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_plan_email():
    sender_email = os.environ.get('SENDER_EMAIL')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')
    aws_region = os.environ.get('AWS_DEFAULT_REGION', 'eu-west-2')
    
    if not sender_email or not recipient_email:
        print("Error: SENDER_EMAIL and RECIPIENT_EMAIL must be set")
        sys.exit(1)

    try:
        with open('tfplanfile.txt', 'r') as f:
            plan_content = f.read()
    except FileNotFoundError:
        print("Error: tfplanfile.txt not found")
        sys.exit(1)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Terraform Plan Review - {os.getenv('GITHUB_REPOSITORY', 'Unknown Repo')}"

    body = f"""
Terraform Plan Review Required

Repository: {os.getenv('GITHUB_REPOSITORY')}
Run ID: {os.getenv('GITHUB_RUN_ID')}
Branch: {os.getenv('GITHUB_REF_NAME')}
Commit: {os.getenv('GITHUB_SHA')}

Please review the attached Terraform plan before applying.

Workflow URL: https://github.com/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}
"""

    msg.attach(MIMEText(body, 'plain'))

    with open('tfplanfile.txt', 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='txt')
        attachment.add_header('Content-Disposition', 'attachment', filename='terraform-plan.txt')
        msg.attach(attachment)

    try:
        ses = boto3.client('ses', region_name=aws_region)
        response = ses.send_raw_email(
            Source=sender_email,
            Destinations=[recipient_email],
            RawMessage={'Data': msg.as_string()}
        )
        print(f"Plan email sent. Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    send_plan_email()