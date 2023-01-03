import boto3
import string
import random


class BOTO3Client:
    def __init__(self, connection, configuration):
        region_name = connection.get('region')
        auth = configuration.get('auth')
        aws_access_key_id = auth.get('aws_access_key_id')
        aws_secret_access_key = auth.get('aws_secret_access_key')
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
                assume_role_external_id = auth.get('aws_assume_role_external_id')
                prefix = 'AWS_'
                letters = string.ascii_lowercase
                role_session_name = prefix + ''.join(random.sample(letters, 4))
                if assume_role_external_id:
                    response = client.assume_role(
                        RoleArn=role_to_assume_arn,
                        RoleSessionName=role_session_name,
                        ExternalId=assume_role_external_id
                    )
                else:
                    response = client.assume_role(
                        RoleArn=role_to_assume_arn,
                        RoleSessionName=role_session_name
                    )
                aws_creds = response['Credentials']
                self.athena_client = boto3.client('athena',
                                                  aws_access_key_id=aws_creds['AccessKeyId'],
                                                  aws_secret_access_key=aws_creds['SecretAccessKey'],
                                                  aws_session_token=aws_creds['SessionToken'],
                                                  region_name=region_name
                                                  )
                self.s3_client = boto3.client('s3',
                                              aws_access_key_id=aws_creds['AccessKeyId'],
                                              aws_secret_access_key=aws_creds['SecretAccessKey'],
                                              aws_session_token=aws_creds['SessionToken'],
                                              region_name=region_name
                                              )
            else:
                # basic client object authentication with access_key and aws_secret_access_key.
                self.athena_client = boto3.client('athena',
                                                  aws_access_key_id=aws_access_key_id,
                                                  aws_secret_access_key=aws_secret_access_key,
                                                  region_name=region_name
                                                  )
                self.s3_client = boto3.client('s3',
                                              aws_access_key_id=aws_access_key_id,
                                              aws_secret_access_key=aws_secret_access_key,
                                              region_name=region_name
                                              )
        except KeyError as e:
            raise e
        except Exception as e:
            raise KeyError(e.args)
