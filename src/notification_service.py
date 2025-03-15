import json

import boto3
import os
from dotenv import load_dotenv


class NotificationService:
    def __init__(self):
        load_dotenv()
        self.sns_client = boto3.client("sns")
        self.sns_topic_arn = os.getenv("SNS_TOPIC_ARN")

    def publish(self, subject, message):
        self.sns_client.publish(
            TopicArn=self.sns_topic_arn,
            Message=json.dumps(message),
            Subject=subject
        )
