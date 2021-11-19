import boto3

class AWSClient:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def get_signed_url(self, s3_url):
        # Get the service client.
        bucket_name, key_name = split_s3_bucket_key(s3_url)
        # Generate the URL to get 'key-name' from 'bucket-name'
        url = self.s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': key_name,
                "RequestPayer": 'requester'
            }
        )
        return url

def split_s3_bucket_key(s3_path):
    """Split s3 path into bucket and key prefix.
    This will also handle the s3:// prefix.
    :return: Tuple of ('bucketname', 'keyname')
    """
    if s3_path.startswith('s3://'):
        s3_path = s3_path[5:]
    return find_bucket_key(s3_path)


def find_bucket_key(s3_path):
    """
    This is a helper function that given an s3 path such that the path is of
    the form: bucket/key
    It will return the bucket and the key represented by the s3 path
    """
    s3_components = s3_path.split('/')
    bucket = s3_components[0]
    s3_key = ""
    if len(s3_components) > 1:
        s3_key = '/'.join(s3_components[1:])
    return bucket, s3_key