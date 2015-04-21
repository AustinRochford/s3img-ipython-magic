from IPython.display import Image

import boto

def s3img(uri):
    if uri.startswith('s3://'):
        uri = uri[5:]

    bucket_name, key_name = uri.split('/', 1)

    conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)
    key = bucket.get_key(key_name)
    data = key.get_contents_as_string()

    return Image(data=data)


def load_ipython_extension(ipython):
    ipython.register_magic_function(s3img, 'line')
