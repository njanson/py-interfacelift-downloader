#!/usr/bin/env python
# Author: elliott.friedman@gmail.com (Elliott Friedman)
#
# This script downloads interfacelift.com wallpapers.  It is intended to be run
# as a cron job to keep your local directory up to date.

# You will need to modify the next 2 variables:

# Browse to the page that has the wallpaper resolution you want and modify the
# line below to match that (eg: modify date, widescreen, 2880x1800, etc):
INDEX = '/wallpaper/downloads/date/widescreen/2880x1800'

# Path to download to (no escaping needed).
DIR = '/Users/friedman/Pictures/Retina Wallpapers'


# You do not need to modify anything below this line.
import logging
import os
import re
import time
import urllib2

URL = 'http://interfacelift.com'
INDEX = '%s%s' % (URL, INDEX)
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 '
      '(KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17')
RE_CODE = r'<a href="/wallpaper/(\w+)/\d+_\w+_%s\.jpg"><img src="' % INDEX.split('/')[-1]
RE_PICS = r'<a href="/wallpaper/\w+/(\d+_\w+_%s\.jpg)"><img src="' % INDEX.split('/')[-1]
EXISTING = set(os.listdir(DIR))
code = ''
count = 1
downloads = 0
logging.basicConfig(
    format=('%(asctime)s.%(msecs)-3d %(filename)s:%(lineno)s]'
            '  %(message)s'), level=logging.DEBUG, datefmt='%m-%d %H:%M:%S')

def Finished():
  logging.info('Downloaded %d wallpapers.  Directory is now up to date.',
      downloads)
  exit()

while True:
  headers = {'User-Agent': UA}
  request = urllib2.Request('%s/index%d.html' % (INDEX, count), None, headers)
  data = urllib2.urlopen(request).read()
  logging.debug('Grabbed %s/index%d.html', INDEX, count)
  if not code:
    code = re.findall(RE_CODE, data)[0]
  pictures = re.findall(RE_PICS, data)
  logging.debug('Found %d wallpapers: %s', len(pictures), ', '.join(pictures))
  for filename in pictures:
    if filename in EXISTING:
      logging.error('%s/%s exists, exiting.', DIR, filename)
      Finished()
    logging.debug('Downloading: %s/wallpaper/%s/%s', URL, code, filename)
    request = urllib2.Request('%s/wallpaper/%s/%s' % (URL, code, filename), None, headers)
    data = urllib2.urlopen(request).read()
    pic_file = open('%s/%s' % (DIR, filename), 'w')
    pic_file.write(data)
    pic_file.close()
    logging.debug('Wrote: %s/%s', DIR, filename)
    downloads += 1
    time.sleep(1)
  if not pictures:
    Finished()
  time.sleep(5)
  count += 1
