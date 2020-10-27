import boto3
import string
import random
import json


class BOTO3Client:
    def __init__(self, connection, configuration):
        region_name = connection.get('region')
        auth = configuration.get('auth')
        aws_access_key_id = auth.get('aws_access_key_id')
        aws_secret_access_key = auth.get('aws_secret_access_key')
        log_group_names = connection.get('log_group_names', {})
        if type(log_group_names) == str:
            if len(log_group_names):
                log_group_names = json.loads(log_group_names)
            else:
                log_group_names = {}
        self.log_group_names = log_group_names

        try:
            if not region_name:
                raise KeyError('Region must be specified')
            if 'aws_iam_role' in auth and auth.get('aws_iam_role'):
                # specific for role based authentication.Links user to role and
                # generates client object with role based Credentials.
                client = boto3.client('sts',
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key,
                                      )
                role_to_assume_arn = auth.get('aws_iam_role')
                prefix = 'AWS_'
                letters = string.ascii_lowercase
                role_session_name = prefix + ''.join(random.sample(letters, 4))
                response = client.assume_role(
                    RoleArn=role_to_assume_arn,
                    RoleSessionName=role_session_name
                )
                aws_creds = response['Credentials']
                self.client = boto3.client('logs',
                                           aws_access_key_id=aws_creds['AccessKeyId'],
                                           aws_secret_access_key=aws_creds['SecretAccessKey'],
                                           aws_session_token=aws_creds['SessionToken'],
                                           region_name=region_name
                                           )
            else:
                # basic client object authentication with access_key and aws_secret_access_key.
                self.client = boto3.client('logs',
                                           aws_access_key_id=aws_access_key_id,
                                           aws_secret_access_key=aws_secret_access_key,
                                           region_name=region_name
                                           )
        except KeyError as e:
            raise e
        except Exception as e:
            raise KeyError(e.args)
