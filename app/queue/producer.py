 
import pika
import json
import os

def send_to_queue(application_dict):
    """
    Sends the application data to the RabbitMQ queue.

    Parameters:
    - application (dict): The application data to be sent to the queue.

    """
    try:
        # Establish connection to RabbitMQ
        rabitMQ_host = os.getenv('RABBITMQ_HOST')        
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabitMQ_host, port=5672))
        channel = connection.channel()

        # Declare the queue (create if not exists)
        channel.queue_declare(queue='loan_applications')

        # Convert application dictionary to JSON string
        message = json.dumps(application_dict)

        # Publish the message to the queue
        
        channel.basic_publish(
            exchange='',
            routing_key='loan_applications',
            body=message
        )

        print(f" [x] Sent application ID: {application_dict['uuid']} to the queue")

    except Exception as e:
        print(f"Error sending message to queue: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the connection
        if 'connection' in locals() and connection.is_open:
            connection.close()
