import argparse
import logging

def get_parser():
    parser = argparse.ArgumentParser(description='Encrypt and Files with Web-Based Keyfiles')
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-e', '--encrypt', dest='encrypt_mode', action='store_true', help='Encrypt the input file')
    mode_group.add_argument('-d', '--decrypt', dest='decrypt_mode', action='store_true', help='Decrypt the input file')
    parser.add_argument('-i', '--input-file', dest='input_file', type=argparse.FileType('r'), help='The file which will be encrypted/decrypted')
    parser.add_argument('-u', '--url', dest='url', help='The URL which will be used to generate the key')
    parser.add_argument('-ih', '--include-headers', dest='include_headers', action='store_true', help='Include response headers in keyfile generation')
    parser.add_argument('-k', '--insecure', dest='verify_ssl', action='store_false', default=None, help='Disable SSL checks')
    parser.add_argument('-o', '--output', dest='output_path', help='Output file path')
    parser.add_argument("-v", "--verbose", dest='verbose', action='store_true', help="increase output verbosity")
    return parser
    
