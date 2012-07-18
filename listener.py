###############################################################################
# initialize the blogs list

# the file is opened with write mode in order to lock out any writers
with open('data/blogs.txt', 'r') as f:
    urls = [line.strip().split(' ') for line in f.xreadlines()]

###############################################################################
# the blog grabber class

import threading
import feedparser
import time

def merge_data(old_data, new_data, key=lambda a:a):
    '''
    Take two lists of items, assume that one is older than the other, and merge
    them in such a way that they form one timeline. The lists are also assumed
    to be sorted.
    '''
    old_cursor = 0
    new_cursor = 0
    ret = []
    while True:
        if old_cursor < len(old_data) and new_cursor < len(new_data):
            old = old_data[old_cursor]
            new = new_data[new_cursor]

            old_key = key(old)
            new_key = key(new)
            if old_key < new_key:
                ret.append(old)
                old_cursor += 1
            elif new_key < old_key:
                ret.append(new)
                new_cursor += 1
            else:
                ret.append(new)
                new_cursor += 1
                old_cursor += 1
        elif old_cursor < len(old_data):
            ret.append(old_data[old_cursor])
            old_cursor += 1
        elif new_cursor < len(new_data):
            ret.append(new_data[new_cursor])
            new_cursor += 1
        else:
            break
    return ret

import random
from termcolor import colored

class Blog(threading.Thread):
    def __init__(self, url, name):
        threading.Thread.__init__(self)
        self.url = url
        self.entries = []
        self.last_data = None
        self.name = name
    def run(self):
        while True:
            print 'fetching data'
            data = feedparser.parse(self.url)
            # if there is any new data, perform a merge and save the current
            # data as the last data
            if self.last_data is None or self.data_is_new(data):
                print 'Have new data for', colored(self.name, 'green')
                self.entries = merge_data(self.entries, data['entries'],
                                          key=lambda e: e['published_parsed'])
                self.last_data = data
            time.sleep(60 + random.randint(0, 60))
    def data_is_new(self, new_data):
        return self.last_data['entries'] != new_data['entries']

###############################################################################
# 

if __name__ == '__main__':
    # line format is (url, name)
    print urls
    blogs = {}
    for item in urls:
        url = item[0]
        name = item[1]
        blog = Blog(url, name)
        blogs[url] = blog
        blog.start()

    '''
    import descend_json

    old = feedparser.parse(urls[0])
    new = feedparser.parse(urls[0])

    print descend_json.descend_print(feedparser.parse(urls[0]))
    '''
