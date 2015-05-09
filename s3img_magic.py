from StringIO import StringIO

from IPython.core.magic import Magics, magics_class, line_magic
from IPython.display import Image

import boto
from boto.exception import S3ResponseError


def parse_s3_uri(uri):
    if uri.startswith('s3://'):
        uri = uri[5:]

    return uri.split('/', 1)


def get_s3_bucket(bucket_name):
    conn = boto.connect_s3()

    return conn.get_bucket(bucket_name)


def get_s3_key(uri):
    bucket_name, key_name = parse_s3_uri(uri)
    bucket = get_s3_bucket(bucket_name)

    return bucket.get_key(key_name)


def get_or_create_s3_key(uri):
    bucket_name, key_name = parse_s3_uri(uri)
    bucket = get_s3_bucket(bucket_name)

    return bucket.new_key(key_name)


def s3img(uri):
    try:
        key = get_s3_key(uri)

        if key is not None:
            data = key.get_contents_as_string()

            return Image(data=data)
        else:
            print "The requested S3 key does not exist."
    except S3ResponseError:
        print "The requestes S3 bucket does not exist."


@magics_class
class S3ImageSaver(Magics):
    @line_magic
    def s3img_save(self, line):
        """BEWARE: this magic will happily overwrite any S3 URI"""
        fig_name, uri = line.split(' ', 1)

        fig = self.shell.ev(fig_name)
        tmp = StringIO()
        fig.savefig(tmp)

        try:
            key = get_or_create_s3_key(uri)
            key.set_contents_from_string(tmp.getvalue())
        except S3ResponseError:
            print "The requestes S3 bucket does not exist."


def load_ipython_extension(ipython):
    ipython.register_magic_function(s3img, 'line')
    ipython.register_magics(S3ImageSaver)
