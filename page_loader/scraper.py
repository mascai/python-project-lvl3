import requests
import logging


logger = logging.getLogger()


def check_url(url):
    if not url.startswith("http"):
        url = "{}{}".format('http://', url.lstrip('./'))
    return url


def get_response(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
        logger.debug("Error during request to {}. Info: {}".format(url, err))
    else:
        logger.debug("Successfull request")
        print(response)
        return response
        

def run_scraper(args):
    #try:
    print("222 {}".format(args))
    url = check_url(args.url)
    print("3333 {}".format(url))
    response = get_response(url)
    print("444")
    #except Exception:
    #    return False
    #else:
    return True
