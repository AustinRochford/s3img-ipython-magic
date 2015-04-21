#!/bin/bash

apt-get update
apt-get install -y python-pip python2.7-dev libzmq-dev
pip install "ipython[notebook]"
pip install boto
