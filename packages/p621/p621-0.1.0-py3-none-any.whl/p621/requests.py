from p621.posts import Post

import requests
from requests import Response

USER_AGENT: str = 'p621/0.1.0'

def search_posts(api_key: str, username: str, limit: int = None, tags: list[str] = None, page: int = None) -> list[Post]:
    parameters: dict = {'api_key': api_key, 'login': username}
    if limit:
        parameters['limit'] = limit
    if tags:
        parameters['tags'] = ' '.join(tags)
    if page:
        parameters['page'] = page

    response: Response = requests.get('https://e621.net/posts.json', params = parameters, headers = {'User-Agent': USER_AGENT})
    posts: dict = response.json()['posts']

    return [Post(post) for post in posts]

def list_favorites(api_key: str, username: str, user_id: int = None) -> list[Post]:
    parameters: dict = {'api_key': api_key, 'login': username}
    if user_id:
        parameters['user_id'] = user_id

    response: Response = requests.get('https://e621.net/favorites.json', params = parameters, headers = {'User-Agent': USER_AGENT})
    posts: dict = response.json()['posts']

    return [Post(post) for post in posts]