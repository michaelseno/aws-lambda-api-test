import json

import boto3
import os
from dotenv import load_dotenv
from datetime import datetime


class NotificationService:
    def __init__(self):
        load_dotenv(override=True)
        self.sns_client = boto3.client("sns",
                                       region_name=os.getenv("AWS_REGION"))
        self.sns_topic_arn = os.getenv("SNS_ARN")

    def publish(self, subject, message):
        self.sns_client.publish(
            TopicArn=self.sns_topic_arn,
            Message=json.dumps(message),
            Subject=f"{subject} - {self.parse_date(date=datetime.now())}"
        )

    @staticmethod
    def parse_date(date):
        return date.strftime("%Y-%m-%d %H:%M:%S")
