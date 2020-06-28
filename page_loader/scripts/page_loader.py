import argparse
import logging
import sys
from page_loader import loader


FORMAT = '%(asctime)s %(message)s' # noqa WPS323
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()


def parse(argv):
    p = argparse.ArgumentParser()
    p.add_argument(
        '-o',
        '--output',
        dest='output_dir',
        default='./',
        help='Output directory',
    )
    p.add_argument(
        '-l',
        '--loglevel',
        dest='loglevel',
        default='INFO',
        help='Log level [DEBUG, INFO, WARNING, ERROR]',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
    )
    p.add_argument('url', metavar='URL')
    return p.parse_args(argv)


def main():
    args = parse(sys.argv[1:])
    logger.setLevel(args.loglevel)
    logger.debug("Start parsing of: {}".format(args.url))
    try:
        loader.parse_url(args.url, args.output_dir)
        logger.debug("Finish parsing of: {}".format(args.url))
    except loader.LoaderError:
        logger.error('Error occurs.')
        sys.exit(1)
    else:
        logger.info('Successfully loaded the page.')


if __name__ == '__main__':
    main()
