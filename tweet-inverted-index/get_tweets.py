import requests
import json
import os


# retrieve Twitter bearer token
# > export 'BEARER_TOKEN'='<your_bearer_token>'
token = os.environ.get("BEARER_TOKEN")


# Documentation: 
# https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-mentions

def create_url():
    """
    Create url for API request. This endpoint returns tweets mentioning a single user.
    """
    # TSEjurbr profile
    user_id = 75270377
    return f"https://api.twitter.com/2/users/{user_id}/mentions"


def get_params(max_results=5):
    """
    Returns query parameters.
    """
    # 'tweet.fields=text' comes by default
    return {
        "tweet.fields": "text,created_at,author_id,entities",
        "max_results": max_results
        }


def oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {token}"
    r.headers["User-Agent"] = "v2UserMentionsPython"
    return r


def connect_endpoint(url, params):
    """
    Makes request to API. Returns a JSON response or error log.
    """
    response = requests.request('GET', url, auth=oauth, params=params)
    print(f"\nResponse status: {response.status_code}")    
    if response.status_code != 200:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}"
        )
    return response.json()
    

def get_tweets():
    """
    Get tweets from endpoint. Return response's first set of tweets and metadata.
    """
    url = create_url()
    params = get_params()
    json_response = connect_endpoint(url, params)
    return json_response


def paginate(url, params, next=""):
    """
    Recursively requests and yields next set of values.
    Gets 'next_token' from metadata of previous 'connect_endpoint()' response.
    """
    if next:
        full_url = f"{url}?pagination_token={next}"
    else:
        full_url = url
    data = connect_endpoint(full_url, params)
    yield data
    if 'next_token' in data.get('meta', {}):
        yield from paginate(url, params, data['meta']['next_token'])


if __name__ == "__main__":
    print(json.dumps(get_tweets(), indent=4, sort_keys=True, ensure_ascii=False))
