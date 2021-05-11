# -*- coding: utf-8 -*-
import os
import boto.s3

DEFAULT_REGION = 'ap-northeast-2'
AWS_S3_HOST = 's3.ap-northeast-2.amazonaws.com'


class S3:
    def __init__(self, access_key, secret_key, region='ap-northeast-2'):
        self.aws_access_key = access_key
        self.aws_secret_key = secret_key
        self.region = region
        self.host = 's3.%s.amazonaws.com' % region

    def get_bucket(self, bucket_name):
        conn = boto.s3.connect_to_region(self.region,
                                         aws_access_key_id=self.aws_access_key,
                                         aws_secret_access_key=self.aws_secret_key,
                                         host=self.host)
        bucket = conn.get_bucket(bucket_name)
        return boto.s3.key.Key(bucket)

    def upload_to_s3_with_filename(self, bucket_name, key, filename, public=False, callback=None, md5=None, reduced_redundancy=False, content_type=None):
        try:
            file = open(filename, 'rb')
            size = os.fstat(file.fileno()).st_size
            return self.upload_to_s3_with_file(bucket_name, key, file, size, public, callback, md5, reduced_redundancy, content_type)
        except Exception:
            return False

    def upload_to_s3_with_file(self, bucket_name, key, file, size, public=False, callback=None, md5=None, reduced_redundancy=False, content_type=None):
        conn = boto.s3.connect_to_region(self.region,
                                         aws_access_key_id=self.aws_access_key,
                                         aws_secret_access_key=self.aws_secret_key,
                                         host=self.host)

        bucket = conn.get_bucket(bucket_name)
        k = boto.s3.key.Key(bucket)
        k.key = key
        if content_type:
            k.set_metadata('Content-Type', content_type)

        sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)
        if public:
            k.set_acl('public-read')

        file.close()

        if sent == size:
            return True
        return False

    def download_file_from_s3(self, bucket, filename, key):
        k = self.get_bucket(bucket)
        if key.startswith('/%s' % bucket):
            key = key.replace('/%s' % bucket, '', 1)

        k.key = key
        k.get_contents_to_filename(filename)

    def get_matching_s3_keys(self, bucket, prefix='', suffix=''):
        conn = boto.s3.connect_to_region(self.region,
                                         aws_access_key_id=self.aws_access_key,
                                         aws_secret_access_key=self.aws_secret_key,
                                         host=self.host)
        bucket = conn.get_bucket(bucket)
        files = []
        for key in bucket.list(prefix=prefix):
            if key.name.endswith(suffix):
                files.append(key.name)

        return files
