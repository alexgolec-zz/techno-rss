def descend(data):
    print descend_print(data)

def descend_print_rec(data, passed_key, ret):
    '''Recursively print out the structure of json-like data.'''
    if isinstance(data,dict):
        for key in data.keys():
            descend_print_rec(data[key], passed_key+'[\''+key+'\']', ret)
    elif isinstance(data,list):
        for i in range(0,len(data)):
            descend_print_rec(data[i], passed_key+'['+str(i)+']', ret)
    else:
        ret.append(passed_key+' = \''+unicode(data)+'\' --- '+str(type(data)))

def descend_print(data):
    '''Returns a string representing the structure of json-like data.'''
    ret = []
    descend_print_rec(data, '', ret)
    return '\n'.join(ret)

import urllib2
import json

def get_data(site):
    return json.loads(urllib2.urlopen(site).read())
