# Social Media Notification System

## Description

This project implements a notification system for a social media platform. It consumes events from Kafka topics, processes them, and sends notifications via AWS SQS.


## Prerequisites

### Setting up Confluent Kafka

1. Download and install Confluent Platform:
   - Visit the [Confluent Platform download page](https://www.confluent.io/download/)
   - Choose the appropriate version for your operating system
   - Follow the installation instructions provided

2. Start Confluent Platform:

confluent local services start


3. Verify the installation:

confluent local services status


### Creating Kafka Topics

1. Create the required topics:

kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transactional
kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic promotional

2. Verify the topics:

kafka-topics --list --bootstrap-server localhost:9092


### AWS Account Setup

1. Create an AWS account if you don't have one: [AWS Console](https://aws.amazon.com/)

2. Set up AWS SQS:
- Open the [Amazon SQS console](https://console.aws.amazon.com/sqs/)
- Click "Create queue"
- Choose a queue name and configure settings
- Note the queue URL for later use

3. Set up AWS SES:
- Open the [Amazon SES console](https://console.aws.amazon.com/ses/)
- Verify your email address or domain
- If your account is in sandbox mode, verify recipient email addresses

4. Set up AWS Lambda:
- Open the [AWS Lambda console](https://console.aws.amazon.com/lambda/)
- Click "Create function"
- Choose a name and runtime (e.g., Python 3.8)
- Configure the function to process messages from SQS and send emails via SES

5. Configure AWS CLI:
- Install AWS CLI: [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- Run `aws configure` and enter your AWS access key ID, secret access key, and default region



## Installation

1. Clone the repository:
git clone https://github.com/ChaitanyaA96/social-media-notification-system.git

2. Install the required dependencies:
pip install -r requirements.txt


## Usage

Run the main script to start the notification system:
python run.py


This will start consuming events from Kafka topics and processing them.

## File Structure

- `run.py`: Main entry point of the application
- `user_db.py`: User database management
- `queue_processor.py`: Processes events from queues
- `queue_manager.py`: Manages different queues for services and topics
- `process_queue.py`: Implementation of the process queue
- `event.py`: Event class and event type definitions
- `aws_sqs.py`: AWS SQS integration for sending messages
- `consumer.py`: Kafka consumer implementation

## Dependencies

- Python 3.7+
- confluent-kafka
- boto3
- sortedcontainers

## Configuration

Ensure you have set up the following configuration:

1. Kafka bootstrap servers
2. Kafka topics
3. AWS credentials
4. AWS SQS URL
5. Schema Registry URL

Update the `keys.py` file with your specific configuration.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
