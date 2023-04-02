import sys
import getpass
import logging
import encrypt
import web
from cli.parser import get_parser
import encrypt
from pathlib import Path

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Handle web options 
    request_options = {'verify_ssl': args.verify_ssl, 'include_headers': args.include_headers}

    # Set paths
    if args.input_path:
        try:
            input_path = Path(args.input_path)
        except Exception as e:
            print(f'Invalid input path: {e}')
            sys.exit(1)
        if not input_path.exists():
            print(f'Error: input path does not exist: {e}')
    else:
        sys.exit("Error: Input file is required. Quitting...")

    if args.output_path:
        try:
            output_path = Path(args.output_path)
        except Exception as e:
            print(f'Invalid output path: {e}')
            sys.exit(1)
    else:
        logging.debug("No output path provided") 

    # If encryption mode
    if args.encrypt_mode:
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