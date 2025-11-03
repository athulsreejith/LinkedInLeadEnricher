import requests
from . import config

def search_linkedin_url(full_name, company):
    params = {
        "engine": "google",
        "q": f"site:linkedin.com/in {full_name} {company}",
        "api_key": config.SERPAPI_KEY,
    }
    r = requests.get("https://serpapi.com/search", params=params, timeout=20)
    r.raise_for_status()
    hits = r.json().get("organic_results", [])
    for h in hits:
        url = h.get("link", "")
        if "linkedin.com/in" in url:
            return url
    return None

def fetch_linkedin_profile(linkedin_url):

    linkedin_id = linkedin_url.rstrip("/").split("/")[-1]
    
    params = {
        "engine": "google",
        "q": f"site:linkedin.com/in {linkedin_id}",
        "api_key": config.SERPAPI_KEY,
    }
    r = requests.get("https://serpapi.com/search", params=params, timeout=20)
    r.raise_for_status()
    data = r.json()

    snippet = ""
    for result in data.get("organic_results", []):
        if "linkedin.com/in" in result.get("link", ""):
            snippet = result.get("snippet", "")
            break

    if not snippet:
        snippet = "No public LinkedIn information available."

    profile_data = {
        "linkedin_url": linkedin_url,
        "summary_text": snippet,
        "experience": [],
        "skills": [],
        "location": "",
    }

    return profile_data
