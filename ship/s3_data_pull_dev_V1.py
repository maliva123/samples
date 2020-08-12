# Import main packages/modules
import boto3
import logging,sys
import logging.handlers
from logging.handlers import SysLogHandler
import os
import json
import gzip
from io import BytesIO
from gzip import GzipFile
from datetime import datetime
from botocore.config import Config
from configs import (user_proxy, aws_configs, exabeam_configs)

# Get the current timestamp
current_date = datetime.now().strftime("%Y%m%d-%H%M%S")


def s3_hook():
    """
    :return: An s3 connection that'll be used in subsequent functions
    """
    try:

        s3_conn = boto3.resource('s3', aws_access_key_id=aws_configs['access_key'],
                                 aws_secret_access_key=aws_configs['secret_key'],
                                 verify=False, config=Config(proxies=user_proxy))

    except Exception as e:
        print(e)

    return s3_conn


def get_s3_bucket(s3_conn):
    """
    :param s3_conn: The s3_connection
    :return: Returns the s3_bucket we are using
    """
    s3_bucket = s3_conn.Bucket(aws_configs['bucket_name'])
    return s3_bucket


def get_key_list(s3_conn, s3_bucket):
    key_list = []
    prefix = 'org_key=7M9F3L9L/year=2020/'
    try:
        for bucket_object in s3_bucket.objects.filter(Prefix=prefix):
            key = bucket_object
            key_list.extend(key)
            #print(key)
    except Exception as e:
        print(e)

    return key_list


def get_bucket(s3_conn):
    key = 'o
    obj = s3_conn.Object(aws_configs['bucket_name'], key)
    return obj


def get_files(s3_conn, obj):
    my_logger = logging.getLogger('MyLogger')
    # We will pass the message as INFO
    my_logger.setLevel(logging.INFO)
    # my_logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address=('', 5))
    my_logger.addHandler(handler)

    sys_log_data = []
    with gzip.GzipFile(fileobj=obj.get()["Body"], mode='rb') as gzip_file:
        contents = gzip_file.readlines()
        for line in contents:
            a = json.loads(line)
            if a['type'] == "endpoint.event.procstart":
                sys_log_data.append(line.decode("utf-8").strip())

    for lines in sys_log_data:
        my_logger.info('%s', lines)


def main():

    #my_logger.critical('this is critical')
    #logging.basicConfig(filename='/Users/e136320/PycharmProjects/s3_to_exabeam_v1/testing_v1.log',
     #                   format='%(asctime)s %(levelname)s %(message)s',
      #                  filemode='w', level=logging.INFO)  # delete filemode variable to have it append to file
    s3_conn = s3_hook()
    s3_bucket = get_s3_bucket(s3_conn)
    obj = get_bucket(s3_conn)
    get_key_list(s3_conn, s3_bucket)
    get_files(s3_conn, obj)


if __name__ == '__main__':
    main()





