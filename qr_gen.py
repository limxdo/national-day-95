#!/usr/bin/env python3

import qrcode
from sys import argv, exit

# if program is run directrly (not a modlue)
if __name__ == "__main__":
    # check shell agument.
    # if not shell arguments, grab url from input
    if (len(argv) -1) == 0:
        url = input("URL: ").strip()

    # if arguments > 2
    elif (len(argv) -1) > 1:
        print("too many arguments")
        exit(2)
    # if need help page
    else:
        if argv[1] == "--help" or argv[1] == "-h":
            print("Usage: ./qr-gen [URL]")
            exit(0)
        # set url from $1 aguments
        url = argv[1].strip()

    img = qrcode.make(url)
    img.save('static/manual/qrcode.png')
    print('qrcode has been saved in \'static/manual/qrcode.png\'')
# if program is modlue 
else:
    # create qr 'for site by ip'
    def create_qr_site(url: str) -> None:
        img = qrcode.make(url.strip())
        img.save('static/img/qr-site.png')
