import tkinter as tk
import ttkbootstrap as ttk
import requests
import sys
import json
from ttkbootstrap.constants import *
from ttkbootstrap import Style


Wikipedia_api_URL = "https://en.wikipedia.org/w/api.php"

def checkResponseStatus(response_code):
    if response_code != 200:
        print("Error: Unable to fetch data from Wikipedia.")
      

def checkRedirectStatus(data):
    if "redirects" in data["query"]:
        redirected_title = data["query"]["redirects"][0]["to"]
        print(f"Redirected to article {redirected_title}")
        return 0
    return 1

def checkExistanceWiki(pages):
    if "-1" in pages:
        print("Error: Wikipedia page not found.")
      
def returnWikiAPI(article_title):
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

def get_recent_changes():
    article_title = input("Please enter the Wikipedia article name: ").strip()
    response = returnWikiAPI(article_title)
    data = response.json()
    pages = data["query"]["pages"]

    checkResponseStatus(response.status_code)
    checkExistanceWiki(pages)
    checkRedirectStatus(data)

    revisionList = []
    revisions = pages[list(pages.keys())[0]]["revisions"]
    for revision in revisions:
        timestamp = revision["timestamp"]
        username = revision["user"]
        revisionList.append(timestamp + " " + username)
        print(f"{timestamp} {username}")
    
def get_recent_changes_1():
    article_title=entry1.get().strip()

    if not article_title:
        no_entry = "Please enter the name of an article you want to search!"
        lblResult["text"] = no_entry
        return
    
    try:
        response = returnWikiAPI(article_title)
        data = response.json()
        pages = data["query"]["pages"]

        # Handle other cases (no page found, network error, etc.)
        if lblResult.cget("text") == "No Wikipedia page found for article_name.\n":
            lblResult["text"] = "No Wikipedia page found for article_name.\n"
        elif lblResult.cget("text") == "Network error occurred.":
            lblResult["text"] = "Network error occurred."

        checkResponseStatus(response.status_code)
        checkExistanceWiki(pages)
        checkRedirectStatus(data)

        revisionList = []
        revisions = pages[list(pages.keys())[0]]["revisions"]
        for revision in revisions:
            timestamp = revision["timestamp"]
            username = revision["user"]
            revisionList.append(timestamp + " " + username)
        lblResult.config(text="\n".join(revisionList))

    except KeyError:
        wrong_article = "Please enter valid article, thanks!"
        lblResult.config(text=wrong_article)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        lblResult.config(text=error_message)
#ttk Bootstrap features

def GUI():
    global entry1
    global lblResult
    app = ttk.Window(title="The latest Wikipedia Article Editions", themename="sandstone") # Creates window
    app.geometry("600x500") # Sets the initial size of the window


    # Apply the Bootstrap theme
    style = Style(theme="darkly")



    # Create a custom style for the Label widget with info style
    style.configure("TLabel", background=style.colors.info, padding=6, font=("Helvetica", 10))

    lbl1 = ttk.Label(app, text="Enter Wikipedia article that you would like to search:")
    lbl1.grid(column=0, row=2)



    # Create a custom style for the Entry widget
    style.configure("TEntry", padding=6, relief="flat",font=("Lato"),fieldbackground=style.colors.dark)

    entry1 = ttk.Entry(app, style="TEntry")
    entry1.grid(column=2, row=2)
    entry1.bind("<Return>", lambda event=None: get_recent_changes_1()) #This code can make searchable when user enter "enter" key

    #This bootstrap "success" color apply on search button
    #It also support for clik and search from a mouse option
    btnSearch = ttk.Button(app, text="Search", style="success.TButton", command=get_recent_changes_1)
    btnSearch.grid(column=3, row=2)


    #All the text will be applied "ttk boot strap warning theme color"
    lblResult = ttk.Label(app, text="", style="warning")
    lblResult.grid(column=0, row=10, columnspan=10)

    app.mainloop()

while True:
    print("Please choose (numbers) below options to search for Wiki articles.")
    print("1. I will search on command line.")
    print("2. I love to use GUI to search.")
    print("3. I'm done for today (Quit.)")

    try:
        option = int(input())

        if option == 1: 
            get_recent_changes()  

        elif option == 2:
            GUI()

        elif option == 3:
            print("Thank You!")
            break

    except ValueError:
        print("Invalid input. Please enter number (1,2, or 3)")