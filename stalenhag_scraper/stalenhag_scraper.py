import os
from datetime import datetime

import urllib.request
from urllib.parse import urljoin

from bs4 import BeautifulSoup

import logging

# TODO: get a logging system!
# create log name
now = datetime.now()
log_name = now.strftime('%d-%m-%Y_%H:%M:%S') + '_stalenhag.log'
# Create custom logger
logger = logging.getLogger(__name__)
# Create log handler (only for file)
f_handler = logging.FileHandler(log_name)
f_handler.setLevel(logging.WARNING)
# Create formatter
f_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_formatter)

logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)


logger.debug('debug on')
logger.info('info on')
logger.warning('warning on')
logger.error('error on')
logger.critical('critical on')

base_url = "http://www.simonstalenhag.se/index.html"
# TODO: Make checking OS agnostic
# folder exist?
if os.path.isdir('./img_stalenhag'):
    logger.warning('img_stalenhag folder found')
else:
    os.mkdir('img_stalenhag')

download_directory = "img_stalenhag"


# Data containers
# Using sets as we don't want to store duplicates
to_visit   = set([base_url])
visited    = set()
downloaded = set()

# While there are url not visited keep 
# going through the list
while to_visit:
    current_page = to_visit.pop()
    logger.info("Woring on: %s", current_page)
    visited.add(current_page)
    content = urllib.request.urlopen(current_page).read()
    
    # Extract any new links from that page
    for link in BeautifulSoup(content, "lxml").findAll("a"):
        # TODO: There should be a more elegant way to identify
        #       when the link is not relative from the base
        #       url
        #
        #   Simon site have paths to his social media / store,
        #   links to his galleries and links to his art work.
        #   For his art work, he uses thumbnails as a link to a
        #   higer resolution image. The following decision tree
        #   ignores absolut links (starting with http & mailto)
        #   
        #   The script downloads all targets of links to a jpg
        #   file.
        #
        if "http" in link["href"]:
            logger.info("Ignoring absolute link: %s", link["href"])
            pass
        elif "mailto" in link["href"]:
            logger.info("Ignoring mailto link: %s", link["href"])
            pass
        elif "jpg" in link["href"]:
            img_href = urljoin(current_page, link["href"])
            if img_href not in downloaded:
                img_name = img_href.split("/")[-1]
                logger.info("Downloading: %s", img_href)
                # TODO: Find a better way to handle broken links
                #       or incomplete requests
                #
                #       Create a sub-folder based on the sub-link 
                #       name to keep images organized
                try:
                    urllib.request.urlretrieve(img_href, os.path.join(download_directory, img_name))
                    downloaded.add(img_href)
                except:
                    logger.error("broken link: %s", img_href)    
            else:
                logger.info("Already Downloaded: %s", img_href)
        else:
            absolute_link = urljoin(base_url, link["href"])
            if absolute_link not in visited:
                logger.info("Adding to_visit set: %s", absolute_link) 
                to_visit.add(absolute_link)
            else:
                logger.info("Already visited: %s", absolute_link)