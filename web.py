import requests
import logging

def get_webpage(url, **request_options):
    verify_ssl = request_options.get('verify_ssl', True)
    include_headers = request_options.get('include_headers', False)
    r = requests.get(url, verify=verify_ssl)
    if not include_headers:
        return r.text.encode('utf-8')
    else: 
        return r.content