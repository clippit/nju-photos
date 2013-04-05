#!/usr/bin/env python

import codecs
import os
import re
import requests
from gevent import monkey
from gevent.pool import Pool


class Downloader(object):
    """Download degree photos"""
    def __init__(self, student_info_file='students.txt', directory='./xwz', big_picture=False, pool_size=20):
        super(Downloader, self).__init__()
        self.student_info_file = student_info_file
        self.directory = directory
        self.pool = Pool(pool_size)
        self.LOGIN_URL = 'http://114.212.186.134/xwz/login.asp'
        if big_picture:
            self.IMAGE_URL = 'http://114.212.186.134/xwz/bigpicture.asp'
        else:
            self.IMAGE_URL = 'http://114.212.186.134/xwz/picture.asp'
        self.downloaded = 0
        self.error = 0

    def run(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        with codecs.open(self.student_info_file, 'r', 'utf-8') as f:
            for line in f:
                sid, name = line.rstrip().split(',', 2)
                self.pool.spawn(self.download, sid, name)
        self.pool.join()

        print "===================="
        print "Downloaded: %d, Error: %d" % (self.downloaded, self.error)

    def download(self, sid, name):
        payload = {'xm': name.encode('GB18030'), 'xh': sid, 'login': 'yes'}
        response = requests.post(
            self.LOGIN_URL,
            data=payload
        )
        download_search = re.search(r"picture\.asp\?i=(\d+)", response.text)
        if download_search is None:
            print '%s not found' % (sid)
            self.error += 1
            return
        download_id = download_search.group(1)
        params = {'i': download_id}
        headers = {'referer': self.LOGIN_URL}
        image = requests.get(
            self.IMAGE_URL,
            params=params,
            headers=headers,
            cookies=response.cookies
        )
        filename = '%s/%s-%s-%s.jpg' % (self.directory, sid, name, download_id)
        with open(filename, 'w') as f:
            f.write(image.content)
        print 'Image for %s saved!' % (sid)
        self.downloaded += 1


if __name__ == '__main__':
    monkey.patch_all(thread=False, select=False)
    Downloader(big_picture=False).run()
