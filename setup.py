try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='s3img-ipython-magic',
    version='0.0.3',
    author="Austin Rochford",
    author_email="austin.rochford@gmail.com",
    description="s3 image line magic for ipython 2 and 3",
    install_requires=['ipython>=2.0', 'boto'],
    keywords="ipython",
    license="MIT",
    long_description="""This package provides a line magics for embedding images from Amazon S3 into an IPython notebook""",
    platforms='any',
    py_modules=['s3img_magic'],
    url="https://github.com/AustinRochford/s3img-ipython-magic",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ]
)
