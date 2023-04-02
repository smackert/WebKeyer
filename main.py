import getpass
import logging
import encrypt
import web
from cli.parser import get_parser
import encrypt


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    request_options = {'verify_ssl': args.verify_ssl, 'include_headers': args.include_headers}

    # If encryption mode
    if args.encrypt:
        logging.debug("Starting in encryption mode")
        # Ask for password and Verify
        while True:
            p = getpass.getpass()
            if (p == getpass(prompt='Verify password:')):
                break
            else:
                print("Passwords do not match!")
        
        # Try to get the webpage if a URL is provided
        webkeyfile = web.get_webpage(args.url, **request_options)
        if webkeyfile:
            password = p.encode('utf-8') + webkeyfile
        else:
            logging.debug("No web keyfile provided.") 
            password = p.encode('utf-8')   
        encrypt(p, args.input_file)