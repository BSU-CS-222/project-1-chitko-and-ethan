import requests
import sys  #Import the sys module
import json #Import the json module in order to exract json data
import ssl #Import the SSL module 
from urllib.request import urlopen #Import the urlopen function from urllib.requests

Wikipedia_api_URL = "https://en.wikipedia.org/w/api.php"
#Wikipedia API endpoint URL

def checkResponseStatus(response_code):
        if response_code != 200:
            print("Error: Unable to fetch data from Wikipedia.")
            
            sys.exit(3)
            
        
def checkRedirectStatus(data):
        if "redirects" in data["query"]:
            redirected_title = data["query"]["redirects"][0]["to"]
            print(f"Redirected to article {redirected_title}")
            return 0
        return 1

def checkExistanceWiki(pages):
     
     if "-1" in pages:
        print("Error: Wikipedia page not found.")
        sys.exit(2)

def checkForValidEntry(entry):
    if len(entry) < 2:
        print("Error: Please provide the name of a Wikipedia article.")
        sys.exit(1)
    

def returnWikiAPI(Wikipedia_api_url, article_title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": article_title,
        "rvlimit": 30,
        "rvprop": "user|timestamp",
    }
    response = requests.get(Wikipedia_api_URL, params=params)
    
    return response

#Define a function for gathering the most recent editions
def get_recent_changes(article_title):
    #Define parameters for the API requests
    

    #Send a Get request to WIKI API with above exact parameters
    #Gather json file from web api
    response = returnWikiAPI(Wikipedia_api_URL,article_title)
    data = response.json()
    pages = data["query"]["pages"]
    


    #Make sure set up for get method web error code not to be equal 200
    checkResponseStatus(response.status_code)

    
    #Make sure artile found in the json 
    #If not found exit error code with print page not found
    checkExistanceWiki(pages)

    #Check and see the search result is in another article
    checkRedirectStatus(data)
    

    #Extract and print the most recent revison of the desire article
    revisionList = []
    revisions = pages[list(pages.keys())[0]]["revisions"]
    for revision in revisions:
        timestamp = revision["timestamp"]
        username = revision["user"]
        revisionList.append(timestamp + " " + username)
        print(f"{timestamp} {username}")
    return revisionList

#In oreder to prevent for code error check and see user import the article
#If import not found, print with error: please provide the name of the wiki articles
if __name__ == "__main__":
    checkForValidEntry(sys.argv)

    #Make sure the command line is to forn the article title
    article_title = " ".join(sys.argv[1:])

    #Call tge function in order to print the most recent wiki article data
    get_recent_changes(article_title)
