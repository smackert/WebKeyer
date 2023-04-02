import requests
import logging

def get_webpage(url, verify_ssl=True, include_headers=False):
    r = requests.get(url, verify=verify_ssl)
    if not include_headers:
        return r.text.encode('utf-8')
    else: 
        return r.content