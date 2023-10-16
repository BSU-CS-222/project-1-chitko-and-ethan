import requests #Import the requests library to make HTTP request
import sys  #Import the sys module
import json #Import the json module in order to exract json data
import ssl #Import the SSL module 
from urllib.request import urlopen #Import the urlopen function from urllib.requests

Wikipedia_api_URL = "https://en.wikipedia.org/w/api.php"
#Wikipedia API endpoint URL

#Define a function for gathering the most recent editions
def get_recent_changes(article_title):
    #Define parameters for the API requests
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": article_title,
        "rvlimit": 30,
        "rvprop": "user|timestamp",
    }

    #Send a Get request to WIKI API with above exact parameters
    response = requests.get(Wikipedia_api_URL, params=params)

    #Make sure set up for get method web error code not to be equal 200
    if response.status_code != 200:
        print("Error: Unable to fetch data from Wikipedia.")
        sys.exit(3)

    #Gather json file from web api
    data = response.json()
    pages = data["query"]["pages"]

    #Make sure artile found in the json 
    #If not found exit error code with print page not found
    if "-1" in pages:
        print("Error: Wikipedia page not found.")
        sys.exit(2)

    #Check and see the search result is in another article
    if "redirects" in data["query"]:
        redirected_title = data["query"]["redirects"][0]["to"]
        print(f"Redirected to article {redirected_title}")

    #Extract and print the most recent revison of the desire articl
    revisions = pages[list(pages.keys())[0]]["revisions"]
    for revision in revisions:
        timestamp = revision["timestamp"]
        username = revision["user"]
        print(f"{timestamp} {username}")

#In oredert to prevent for code error check and see user import the article
#If import not found, print with error: please provide the name of the wiki articles
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide the name of a Wikipedia article.")
        sys.exit(1)

    #Make sure the command line is to forn the article title
    article_title = " ".join(sys.argv[1:])

    #Call tge function in order to print the most recent wiki article data
    get_recent_changes(article_title)
