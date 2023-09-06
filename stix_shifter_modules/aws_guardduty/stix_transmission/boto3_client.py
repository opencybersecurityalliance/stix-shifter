import aioboto3
import string
import random
import botocore


class BOTO3Client:

    def __init__(self, connection, configuration):
        self.connection = connection
        self.configuration = configuration
        self.session = None
        self.timeout = connection['options'].get('timeout')
        self.result_limit = connection['options'].get('result_limit')
        self.verify = False
        self.detector_ids = connection.get('detector_ids', '')

    async def get_session(self):
        """
        Create an AWS GuardDuty Client session for the user.
        :return: session object
        """
        if self.session is None:
            region_name = self.connection.get('region')
            auth = self.configuration.get('auth')
            aws_access_key_id = auth.get('aws_access_key_id')
            aws_secret_access_key = auth.get('aws_secret_access_key')
            try:
                if not region_name:
                    raise KeyError('Region must be specified')
                if 'aws_iam_role' in auth and auth.get('aws_iam_role'):
                    # specific for role based authentication.Links user to role and
                    # generates client object with role based Credentials.
                    session = aioboto3.Session()
                    async with session.client('sts',
                                              aws_access_key_id=aws_access_key_id,
                                              aws_secret_access_key=aws_secret_access_key,
                                              verify=self.verify
                                              ) as client:
                        role_to_assume_arn = auth.get('aws_iam_role')
                        assume_role_external_id = auth.get('aws_assume_role_external_id')
                        prefix = 'AWS_'
                        letters = string.ascii_lowercase
                        role_session_name = prefix + ''.join(random.sample(letters, 4))
                        if assume_role_external_id:
                            response = await client.assume_role(
                                RoleArn=role_to_assume_arn,
                                RoleSessionName=role_session_name,
                                ExternalId=assume_role_external_id
                            )
                        else:
                            response = await client.assume_role(
                                RoleArn=role_to_assume_arn,
                                RoleSessionName=role_session_name
                            )
                        aws_creds = response['Credentials']
                    self.session = aioboto3.Session(
                        aws_access_key_id=aws_creds['AccessKeyId'],
                        aws_secret_access_key=aws_creds['SecretAccessKey'],
                        aws_session_token=aws_creds['SessionToken'],
                        region_name=region_name
                    )
                else:
                    # basic client object authentication with access_key and aws_secret_access_key.
                    self.session = aioboto3.Session(
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name
                    )
            except KeyError as e:
                raise e
            except Exception as e:
                raise KeyError(e.args)

        return self.session

    async def get_paginated_result(self, api_name, method, **kwargs):
        """
        Fetch the results through pagination for the corresponding GuardDuty method.
        :param api_name,str
        :param method,str
        :return: dict containing a list of finding ids/detector ids with next page token
        """
        result_response_list = []
        session = await self.get_session()
        config = botocore.config.Config(
            read_timeout=self.timeout,
            connect_timeout=self.timeout
        )
        async with session.client(api_name, verify=self.verify, config=config) as cl:
            paginator = cl.get_paginator(method)
            get_query_response = paginator.paginate(**kwargs)
            async for page in get_query_response:
                if page.get('ResponseMetadata').get('HTTPStatusCode') == 200:
                    if page.get('DetectorIds'):
                        result_response_list.extend(page.get('DetectorIds'))
                    elif page.get('FindingIds'):
                        result_response_list.extend(page.get('FindingIds'))
                else:
                    return page['ResponseMetadata']
        result_dict = {'data': result_response_list, 'next_token': page.get('NextToken')}
        return result_dict

    async def make_request(self, api_name, method, **kwargs):
        """
        Fetch the results for the corresponding GuardDuty method
        :return: Response object
        """
        session = await self.get_session()
        config = botocore.config.Config(
            read_timeout=self.timeout,
            connect_timeout=self.timeout
        )
        async with session.client(api_name, verify=self.verify, config=config) as cl:
            call = getattr(cl, method.lower())
            response = await call(**kwargs)
        return response
