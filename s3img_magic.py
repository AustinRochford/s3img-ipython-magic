from IPython.display import Image

import boto

def parse_s3_uri(uri):
    if uri.startswith('s3://'):
        uri = uri[5:]

    return uri.split('/', 1)


def get_s3_key(uri):
    bucket_name, key_name = parse_s3_uri(uri)

    conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)

    return bucket.get_key(key_name)


def s3img(uri):
    key = get_s3_key(uri)
    data = key.get_contents_as_string()

    return Image(data=data)


def load_ipython_extension(ipython):
    ipython.register_magic_function(s3img, 'line')
