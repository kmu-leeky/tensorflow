# a function to check if interrupted
# a function to query to initiate migration
#

import pycurl
import re
from StringIO import StringIO
import tinys3
import os

interrupt_check_url = "http://169.254.169.254/latest/meta-data/spot/termination-time"

def check_if_interrupted() :
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, interrupt_check_url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    return bool(re.search('.*T.*Z', body))

def upload_checkpoint_to_s3(source_file, bucket):
    conn = tinys3.Connection(os.environ["AWS_ACCESS_KEY_ID"], os.environ["AWS_SECRET_ACCESS_KEY"], tls=True)
    f = open(source_file, 'rb')
    conn.upload(source_file, f, bucket)
    