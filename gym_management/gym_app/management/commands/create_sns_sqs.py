from django.core.management.base import BaseCommand

from common.aws.boto_sessions.session_manager import get_boto_client


class Command(BaseCommand):
    help = 'Create multiple SNS topics and SQS queues, and subscribe SQS to each topic.'

    def handle(self, *args, **kwargs):
        sns_client = get_boto_client('sns')
        sqs_client = get_boto_client('sqs')

        # Create SNS Topics
        topics = ['Topic1', 'Topic2', 'Topic3']
        topic_arns = {}
        for topic in topics:
            response = sns_client.create_topic(Name=topic)
            topic_arn = response['TopicArn']
            topic_arns[topic] = topic_arn
            self.stdout.write(self.style.SUCCESS(f'Topic created: {topic_arn}'))

        queues = ['Queue1', 'Queue2']
        queue_urls = {}
        queue_arns = {}
        for queue in queues:
            response = sqs_client.create_queue(QueueName=queue)
            queue_url = response['QueueUrl']
            queue_urls[queue] = queue_url
            self.stdout.write(self.style.SUCCESS(f'Queue created: {queue_url}'))

            attrs = sqs_client.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['QueueArn']
            )
            queue_arn = attrs['Attributes']['QueueArn']
            queue_arns[queue] = queue_arn
            self.stdout.write(self.style.SUCCESS(f'Queue ARN: {queue_arn}'))

        for topic in topics:
            for queue in queues:
                sns_client.subscribe(
                    TopicArn=topic_arns[topic],
                    Protocol='sqs',
                    Endpoint=queue_arns[queue]
                )
                self.stdout.write(self.style.SUCCESS(f'Subscribed {queue} to {topic}'))
