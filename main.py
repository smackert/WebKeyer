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

    if encrypt:
        # Ask for password and Verify
        while True:
            p = getpass.getpass()
            if (p == getpass(prompt='Verify password:')):
                break
            else:
                print("Passwords do not match!")
        
        # Try to get the webpage if a URL is provided
        webkeyfile = web.get_webpage(url, **request_args)
        if webkeyfile:
            password = p.encode('utf-8') + webkeyfile
        else:
            logging.debug("No web keyfile provided.") 
            password = p.encode('utf-8')   
        encrypt(password, input_file)

# Generate keyfile
webkeyfile = web.get_webpage(arg.url, arg.verify_ssl, arg.include_headers)