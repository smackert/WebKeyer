import sys
import getpass
import logging
from encrypt import encrypt
from decrypt import decrypt
import web
from cli.parser import get_parser
from pathlib import Path


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Handle web options
    request_options = {
        "verify_ssl": args.verify_ssl,
        "include_headers": args.include_headers,
    }

    # Set paths
    if args.input_file:
        try:
            input_file = Path(args.input_file)
        except Exception as e:
            print(f"Invalid input file: {e}")
            sys.exit(1)
        if not input_file.is_file():
            print(f"Error: input file does not exist or cannot be read: {e}")
    else:
        sys.exit("Error: Input file is required.")

    if args.output_path:
        try:
            output_path = Path(args.output_path)
        except Exception as e:
            print(f"Invalid output path: {e}")
            sys.exit(1)
    else:
        logging.debug("No output path provided, defaulting to path of input_file.")
        output_path = input_file

    # If encryption mode
    if args.encrypt_mode:
        logging.debug("Starting in encryption mode")

        # Give file WebKeyer encrypted-file suffix
        output_path = output_path.with_suffix(input_file.suffix + ".wbkr")

        # Ask for password and verify
        while True:
            p = getpass.getpass()
            if p == getpass.getpass(prompt="Verify password:"):
                break
            else:
                print("Passwords do not match!")

        # Skip if there is no URL provided
        if args.url:
            webkeyfile = web.get_webpage(args.url, **request_options)
            if webkeyfile:
                password = p.encode("utf-8") + webkeyfile
            else:
                sys.exit("A URL was provided but the webkey returned None")
        else:
            logging.debug("No web keyfile provided.")
            password = p.encode("utf-8")
        encrypt(p, input_file, output_path)

    # If decryption mode
    if args.decrypt_mode:
        logging.debug("Starting in decryption mode")

        output_path = input_file.stem

        # Ask for pass 
        p = getpass.getpass()

        # Skip if there is no URL provided
        if args.url:
            webkeyfile = web.get_webpage(args.url, **request_options)
            if webkeyfile:
                password = p.encode("utf-8") + webkeyfile
            else:
                sys.exit("A URL was provided but the webkey returned None")
        else:
            logging.debug("No web keyfile provided.")
            password = p.encode("utf-8")
        decrypt(p, input_file, output_path)


if __name__ == "__main__":
    # Call the main function
    main()
