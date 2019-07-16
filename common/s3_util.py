import boto3
from urllib.parse import urlparse

# create an STS client object that represents a live connection to the
# STS service

class S3Util(object):

    def __init__(self, role_arn=None):
        self.role_arn = role_arn

    def get_s3_resource_from_key(self,aws_access_key,aws_secrete_key):
        s3_resource = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secrete_key

        )

        return s3_resource

    def get_s3_resource_from_assumed_role(self):
        sts_client = boto3.client('sts')

        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        assumed_role_object = sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName="AssumeRoleSession1"
        )

        # From the response that contains the assumed role, get the temporary
        # credentials that can be used to make subsequent API calls
        credentials = assumed_role_object['Credentials']

        # Use the temporary credentials that AssumeRole returns to make a
        # connection to Amazon S3
        s3_resource = boto3.resource(
            's3',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )
        return s3_resource

    def read_buckets(self):
        # Use the Amazon S3 resource object that is now configured with the
        # credentials to access your S3 buckets.
        s3_resource = self.get_s3_resource_from_key()
        for bucket in s3_resource.buckets.all():
            print(bucket.name)

    def push_io_bytes_to_s3(self,key,bucket_name,io_bytes):
        s3_resource=self.get_s3_resource_from_key()
        object = s3_resource.Object(bucket_name, key)
        object.upload_fileobj(io_bytes)



    def get_bucket_and_key_from_url(self,url):

        parsed_url = urlparse(url)
        return parsed_url.hostname.split(".")[0],parsed_url.path[1:]

    def delete_file_from_s3(self,url):
        s3_resource = self.get_s3_resource_from_key()
        bucket,key=self.get_bucket_and_key_from_url(url)
        s3_resource.Object(bucket, key).delete()


if __name__ == '__main__':
    S3Util().read_buckets()
# import boto3
# s3 = boto3.client('s3')
# bucket_name = "YOUR-BUCKET-NAME"
# directory_name = "DIRECTORY/THAT/YOU/WANT/TO/CREATE" #it's name of your folders
# s3.put_object(Bucket=bucket_name, Key=(directory_name+'/'))
