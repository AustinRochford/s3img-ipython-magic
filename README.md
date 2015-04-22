# s3img-ipython-magic
An IPython magic that displays images stored in Amazon S3.  I find this useful when running a notebook server on a transient resource (AWS, virtual machine, etc.).

## Demo

![Demo](https://raw.githubusercontent.com/AustinRochford/s3img-ipython-magic/master/s3img_demo.png)

## Usage

* The line magic `%s3img s3_uri` will display the image at the URI `s3_uri` in S3.
* The line magic `%s3img_save fig s3_uri` will save the `matplotlib` figure `fig` to the URI `s3_uri` in S3.

## Installation

To install, do `pip install s3img-ipython-magic` or `%load_ext https://github.com/AustinRochford/s3img-ipython-magic/s3img_magic.py`.

The only dependency (other that IPython) is `boto`.

Your AWS credentials will be read from the environment.

## License

This code is distributed under the [MIT License](https://raw.githubusercontent.com/AustinRochford/s3img-ipython-magic/master/LICENSE).
