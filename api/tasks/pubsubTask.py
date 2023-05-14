import logging
import datetime
import json
import os
from celery import Celery
from ..utils import convert_targz_to_zip, convert_tarbz2_to_zip2
from ..utils import generate_filename, get_filename
from ..models import db, Task, EnumStatusType

from google.cloud import pubsub_v1

# Set up Google Cloud Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('miso-mobile-2023', 'tasks')

BUCKET_NAME = 'converter-storage/'
TEMP_FOLDER = 'files/'

# Define a callback function to handle incoming messages
def callback(message):
    logging.info("Received message: {message.data.decode()}")
    try:
        message_data = message.data.decode()
        message_json = json.loads(message_data)
        task_id = message_json['task_id']
        file_name = message_json['file_name']
        time_stamp = message_json['time_stamp']
        format = message_json['format']
        new_format = message_json['new_format']

        print('taskId=' + task_id + ' - Task register_convert_task starts')
        print('taskId=' + task_id + ' - Request to convert file: ' + file_name +
              ' from ' + format + ' to ' + new_format)
        old_file = BUCKET_NAME + get_filename(file_name, time_stamp, format)
        new_file = generate_filename(task_id, file_name, new_format)

        print('taskId=' + task_id + ' - Convert starts')
        if (format == '.tar.gz' and new_format == '.zip'):
            convert_targz_to_zip(task_id, old_file, new_file)
        if (format == '.tar.bz2' and new_format == '.zip'):
            convert_tarbz2_to_zip2(task_id, old_file, new_file)
        print('taskId=' + task_id + ' - Convert finish')
        print('taskId=' + task_id + ' - Updating task id: ' + task_id)

        # TODO: update task status
        # task = Task.query.get_or_404(int(task_id))
        # task.status = EnumStatusType.PROCESSED
        # task.updated_at = datetime.datetime.utcnow
        # db.session.commit()

        print('taskId=' + task_id + ' - Updated to: ' +
              str(EnumStatusType.PROCESSED))
        print('taskId=' + task_id + ' - Task register_convert_task completed')
        message.ack()
        return True
    except:
        return False
    # Acknowledge the message to remove it from the subscription

def listenForMessages():
    # Subscribe to the topic and start listening for messages
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('miso-mobile-2023', 'tasks-sub')
    subscriber.subscribe(subscription_path, callback=callback)

    # Run the application indefinitely to continuously receive messages
    logging.info("Listening for messages...")
    while True:
        pass