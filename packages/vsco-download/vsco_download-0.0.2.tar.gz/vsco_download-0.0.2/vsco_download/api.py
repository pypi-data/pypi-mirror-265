'''
# VSCO Downloader

A wrapper package for VSCO endpoints

'''
from io import BufferedWriter
from requests import Session
import requests

class VscoMedia:
    '''
    Wrapper for VSCO media. 

    Supply `download_to` with a byte file writer to download.

    Use `is_image` to determine mime/extension.
    '''

    def __init__(self, session: Session, download_url: str,
                 timestamp: int, is_image: bool):
        self.session = session
        self.download_url = download_url
        self.timestamp = timestamp
        self.is_image = is_image

    def download_to(self, writer: BufferedWriter):
        '''
        Supply a byte output stream to `writer`.

        Example: `open('filename.txt', 'wb')`

        Use `is_image` to determine mime/extension.
        '''
        response = self.session.get(self.download_url)
        response.raise_for_status()
        writer.write(response.content)


class VscoApi:
    '''
    A wrapper for VSCO endpoints.
    
    Avoid rate limits by waiting between requests.
    
    Call `set_bearer_token` if you want to avoid using the guest bearer token.
    
    There may be limits associated with the guest bearer token. idk.
    
    To get a bearer token:
    1) Log in to VSCO
    2) Open Inspect Element
    3) Go to Network
    4) Visit some VSCO page
    5) Find a request that has your account's bearer token in its headers.
    '''
    headers = {
        'authority': 'vsco.co',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer 718e4b5e8377b7278deddae99e2d44d67e197786',
        'content-type': 'application/json',
        'dnt': '1',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'x-client-build': '1',
        'x-client-platform': 'web'
        }

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = VscoApi.headers
        self.page_size = 20
        
    def set_bearer_token(self, token: str):
        '''
        To get a bearer token:
        1) Log in to VSCO
        2) Open Inspect Element
        3) Go to Network
        4) Visit some VSCO page
        5) Find a request that has your account's bearer token in its headers.
        '''
        headers = self.session.headers
        headers['authorization'] = token
        
    def set_page_size(self, page_size: int):
        '''
        Set the max amount of posts that are return per request. 30 is max.
        
        Page size >= 30 can sometimes make it where pages past the first aren't served.
        '''
        self.page_size = page_size

    def get_site_id(self, username: str, true_match: bool = True) -> str:
        '''
        Returns the site id for profile with username `username`.

        Raises `ValueError` if `true_match = True` and no profile is found with the exact username.

        Raises `ValueError` if no profile is found.

        Calls `Response.raise_for_status()`
        '''
        response = self.session.get(
            f'https://vsco.co/api/2.0/search/grids?query={username}&page=0&size=7')
        response.raise_for_status()
        for profile in response.json()['results']:
            if true_match:
                if profile['siteSubDomain'] == username:
                    return profile['siteId']
            else:
                return profile['siteId']
        raise ValueError
    type cursor_string = str
    def get_media_page(self, site_id: str, cursor: str | None = None) -> tuple[list[VscoMedia], cursor_string]:
        '''
        Get a site_id for a profile with `VscoWrapper.get_site_id`.
        
        Only returns one page of posts.
        
        If you want multiple pages, iterate through `get_media_cursor()`
        
        '''
        url = f'https://vsco.co/api/3.0/medias/profile?site_id={site_id}&limit={self.page_size}'
        if cursor is not None:
            url = url + f'&cursor={cursor}'
        response = self.session.get(url)
        response.raise_for_status()
        json = response.json()
        medias = [

            VscoMedia(
                self.session, f'https://{info['responsive_url']}', info['upload_date'], True)

            if not info['is_video'] else

            VscoMedia(
                self.session, f'https://{info['video_url']}', info['upload_date'], False)

            for info in map(lambda x: x[x['type']], json['media'])

        ]
        return (medias, json.get('next_cursor'))
 
    def get_media_cursor(self, site_id: str):
        '''
        Iterate through this to get multiple pages.
        
        For just one page, `get_media_page` with None cursor, or 
        just break after 1 iteration.
        '''
        return VscoMediaCursor(site_id, self)

class VscoMediaCursor:
    '''
    Obtain this from vsco module.
    '''
    def __init__(self, site_id: str, wrapper: VscoApi):
        self.cursor = None
        self.medias = []
        self.site_id = site_id
        self.wrapper = wrapper

    def __iter__(self):
        self.medias = []
        return self

    def __next__(self):
        old_cursor = self.cursor
        self.medias, self.cursor = self.wrapper.get_media_page(self.site_id, self.cursor)
        if self.cursor == old_cursor:
            raise StopIteration
        return self.medias
