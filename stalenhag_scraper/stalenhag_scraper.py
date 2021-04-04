import os
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup


# TODO: get a logging system!

base_url = "http://www.simonstalenhag.se/index.html"
# TODO: Check if 'download_directory' exist, if not, 
#       create it in the current working directory
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
    print("Woring on: ", current_page)
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
            print ("Ignoring absolute link: ", link["href"])
            pass
        elif "mailto" in link["href"]:
            print ("Ignoring mailto link: ", link["href"])
            pass
        elif "jpg" in link["href"]:
            img_href = urljoin(current_page, link["href"])
            if img_href not in downloaded:
                img_name = img_href.split("/")[-1]
                print("Downloading: ", img_href)
                # TODO: Find a better way to handle broken links
                #       or incomplete requests
                #
                #       Create a sub-folder based on the sub-link 
                #       name to keep images organized
                try:
                    urllib.request.urlretrieve(img_href, os.path.join(download_directory, img_name))
                    downloaded.add(img_href)
                except:
                    print ("Error")    
            else:
                print("Already Downloaded: ", img_href)
        else:
            absolute_link = urljoin(base_url, link["href"])
            if absolute_link not in visited:
                print("Adding to_visit set: ", absolute_link) 
                to_visit.add(absolute_link)
            else:
                print("Already visited: ", absolute_link)
print("Finish!")