import unittest
from unittest.mock import patch
import sys
import configparser
import os
from s3shell import S3Func

def get_config():
    config = configparser.ConfigParser()

    try:
        with open(os.path.expanduser('~')+'/.s3shell.conf') as f:
            config.read_file(f)
    except Exception as e:
        print('Could not read the config file, make sure it exists and formatted correctly. {}'.format(e))
        sys.exit(1)
    
    return config

class TestS3Func(unittest.TestCase):
    def setUp(self):
        self.access_key = get_config()['default']['aws_access_key_id']
        self.secret_key = get_config()['default']['aws_secret_access_key']
        self.region = get_config()['default']['region']

    @patch('S3Func.boto3.Session')
    def test_init(self, mock_session):
        mock_session.return_value.client.return_value.list_buckets.return_value = {'Buckets': [{'Name': 'test_bucket'}]}
        s3 = S3Func(self.access_key, self.secret_key, self.region)
        self.assertTrue(s3.hasBuckets)

    def test_parsePath(self):
        s3 = S3Func(self.access_key, self.secret_key, self.region)
        parsed_path = s3._S3Func__parsePath('test_path')
        self.assertEqual(parsed_path, '/test_path')

    # Add more tests for other methods as needed

if __name__ == '__main__':
    unittest.main()
