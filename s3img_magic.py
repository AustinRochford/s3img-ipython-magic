from StringIO import StringIO
from warnings import warn

from IPython.core.magic import Magics, line_magic, magics_class, needs_local_scope
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


@magics_class
class S3ImageMagic(Magics):
    def __init__(self, shell):
        super(S3ImageMagic, self).__init__(shell)

        self._s3_base_uri = None

    def _get_s3_uri(self, uri):
        if self._s3_base_uri is not None:
            return '/'.join((self._s3_base_uri, uri))
        else:
            return uri

    @line_magic
    def s3img(self, uri):
        """
        %s3img s3_uri

        Display the image at s3_uri
        """
        try:
            s3_uri = self._get_s3_uri(uri)
            key = get_s3_key(s3_uri)

            if key is not None:
                data = key.get_contents_as_string()

                return Image(data=data)
            else:
                print "The requested S3 key does not exist."
        except S3ResponseError:
            print "The requestes S3 bucket does not exist."

    @needs_local_scope
    @line_magic
    def s3img_save(self, line, local_ns=None):
        """
        %s3img_save fig s3_uri

        Saves the matplotib figure fig to s3_uri

        BEWARE: this magic will happily overwrite any S3 uri
        """
        fig_name, uri = line.split(' ', 1)
        s3_uri = self._get_s3_uri(uri)

        if local_ns is not None and fig_name in local_ns:
            fig = local_ns[fig_name]
            tmp = StringIO()
            fig.savefig(tmp)

            try:
                key = get_or_create_s3_key(s3_uri)
                key.set_contents_from_string(tmp.getvalue())
            except S3ResponseError:
                print "The requested S3 bucket does not exist."
        else:
            print "No figure with the name {} exists in the local scope".format(fig_name)

    @line_magic
    def s3img_base_uri(self, line):
        """
        %s3img_base_uri [s3_uri]

        If s3_uri is given, set it to be the base S3 URI.  All subsequent uses
        of S3 image magics will create their destinations relative to this URI.

        If s3_uri is not given, print the current S3 base URI.
        """
        if line == '':
            if self._s3_base_uri is None:
                print "There is no S3 base URI set"
            else:
                print "The S3 base URI is {}".format(self._s3_base_uri)
        else:
            if self._s3_base_uri is not None:
                warn("Setting the S3 base URI more than once in a notebook may lead to unexpected behavior.")

            self._s3_base_uri = line.rstrip('/')


def load_ipython_extension(ipython):
    ipython.register_magics(S3ImageMagic)
