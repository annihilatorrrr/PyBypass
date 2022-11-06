import requests 
import json
import re


"""
https?://(www\.solidfiles\.com/v/)\S+
http://www.solidfiles.com/v/WqL3V2QjdmDZv
"""

def solidfiles_bypass(url: str) -> str:
    json_file = re.search(r"'viewerOptions\'\,\ (.*?)\)\;", requests.get(url).text)
    return json.loads(json_file[1])["downloadUrl"]
   
    
