
from SimplerLLM.tools.rapid_api import RapidAPIClient
from SimplerLLM.tools.generic_loader import load_content
import httpx


def search_wikipedia(query):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]



def load_content_from_url(url:str):
    """
    Load content from a given URL.
    :param url: str, URL to load content from
    :return: str, content
    """
    content = load_content(url)
    return content.content



def seo_audit_web_page(url :str):
    api_url = "https://website-seo-analyzer.p.rapidapi.com/seo/seo-audit-basic"
    api_params = {
        'url': url,
    }
    api_client = RapidAPIClient() 
    response = api_client.call_api(api_url, method='GET', params=api_params)
    return response


