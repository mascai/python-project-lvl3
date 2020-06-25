import sys
import argparse
from page_loader.scraper import run_scraper

def parse(argv):
    p = argparse.ArgumentParser()
    p.add_argument("-o", "--output", default="./", type=str, help="Result directory")
    p.add_argument("url", type=str)
    return p.parse_args(argv)
    

def main():
    args = parse(sys.argv[1:])
    print("1111")
    if not run_scraper(args):
        sys.exit(1)


if __name__ == '__main__':
    main()
