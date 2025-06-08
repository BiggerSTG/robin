from crewai.tools import BaseTool
import requests
from typing import Any, Dict
from dotenv import load_dotenv
import os

load_dotenv()

#-------------------------------#
#-------------------------------#
##          Tools
#-------------------------------#
#-------------------------------#

#-------------------------------#
## Media Tool
#-------------------------------#
class MediaTool(BaseTool):
    name: str = "Educational Media Fetcher"  # Add type annotation
    description: str = "Fetches educational media content from Freepik."

    def _run(self, query: str) -> Dict[str, Any]:  # Specify input and output types
        """Fetch educational media content from Freepik."""
        if not isinstance(query, str):
            return {"Error": "Please provide a valid query string."}

        url = f"https://api.freepik.com/v1/resources"
        
        params = {
            "term": query,
            "limit": 10,
            "order": "relevance"
        }

        headers = {"x-freepik-api-key": os.getenv("FREEPIK_API_KEY")}
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["data"]:
                return data["data"][0].get("image", "")["source"]["url"]
            else:
                return "No image found."
        else:
            return "Error fetching media content."

# def wikimedia_auth():
#     """Authenticate with Wikimedia API."""
    
#     # Get Login Information
#     client_id = os.getenv("WIKIMEDIA_CLIENT_ID")
#     client_secret = os.getenv("WIKIMEDIA_CLIENT_SECRET")

#     url = "https://meta.wikimedia.org/w/rest.php/oauth2/access_token"
#     params = {
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "grant_type": "client_credentials"
#     }

#     # Headers to ensure form-data encoding
#     headers = {
#     "Content-Type": "application/x-www-form-urlencoded"
#     }

#     response = requests.post(url, data=params, headers=headers)
#     if response.status_code == 200:
#         access_token = response.json().get("access_token")
#         print("Successfully authenticated with Wikimedia API.")
#         return access_token
#     else:
#         return None
    
#Authentication Token for Wikimedia API
# wiki_access_token = wikimedia_auth()

# url = f"https://commons.wikimedia.org/w/api.php"
# params = {
#             "action": "query",
#             "format": "json",
#             "list": "search",
#             "srsearch": "cell division",
#             "srlimit": 10,
#             "srprop": "snippet|titlesnippet",
#             "srnamespace": 6  # Namespace for files
# }
# headers = {
#     "Authorization": f"Bearer {wiki_access_token}"
# }

# response = requests.get(url, params=params, headers=headers)
# if response.status_code == 200:
#     data = response.json()
#     #print("data:", data)
#     media_data = []
#     for result in data["query"]["search"]:
#         title = result["title"]
#         snippet = result["snippet"]
#         file_url = f"https://commons.wikimedia.org/wiki/{title.replace(' ', '_')}"
#         media_data.append({ "file_url": file_url})

#     print("media:", media_data)
# else:
#     print("Could not fetch media content.")


# # Define the custom media tool
# class MediaTool(BaseTool):
#     name: str = "Educational Media Fetcher"  # Add type annotation
#     description: str = "Fetches educational media content from Wikimedia."

#     def _run(self, query: str) -> Dict[str, Any]:  # Specify input and output types
#         """Fetch educational media content from Wikimedia."""
#         if not isinstance(query, str):
#             return {"Error": "Please provide a valid query string."}

#         url = f"https://commons.wikimedia.org/w/api.php"
#         params = {
#             "action": "query",
#             "format": "json",
#             "list": "search",
#             "srsearch": query,
#             "srlimit": 10,
#             "srprop": "snippet|titlesnippet",
#             "srnamespace": 6,  # Namespace for files
#             "srapi": WIKIMEDIA_API_KEY
#         }
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             data = response.json()
#             media_data = []
#             for result in data["query"]["search"]:
#                 title = result["title"]
#                 snippet = result["snippet"]
#                 media_data.append({"title": title, "snippet": snippet})
#             return {"media": media_data}
#         else:
#             return {"Error": "Could not fetch media content."}