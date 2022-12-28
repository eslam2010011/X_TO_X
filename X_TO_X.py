import argparse
import configparser
from services.Apollo import Apollo

END = '\033[0m'

config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")


def print_banner():
    banner = \
        ''''
    db    db         d888888b  .d88b.          db    db 
    `8b  d8'         `~~88~~' .8P  Y8.         `8b  d8' 
     `8bd8'             88    88    88          `8bd8'  
     .dPYb.             88    88    88          .dPYb.  
    .8P  Y8.            88    `8b  d8'         .8P  Y8. 
    YP    YP C88888D    YP     `Y88P'  C88888D YP    YP 
        '''''

    txt_color = 115
    print('\r')

    for line in banner.splitlines():
        color = f'\033[38;5;{txt_color}m'
        print(f'{color}{line}{END}')
        txt_color += 1

    print(f'\t\t\t\t\t           Created by https://github.com/eslam2010011\n')


def args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-d", "--domain", dest="domain", default=None,
                        help="Domain name")
    parser.add_argument("-l", "--list", dest="list", default="a", choices=['j', 'p', 'a', 'o'],
                        help='list all (a), jobs (j), people (p), only_Information (o)   or both (default: %(default)s)')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print_banner()
    args = args()
    Apollo(config, args).run()
