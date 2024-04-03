# Python Vsco Downloader

## Disclaimer
Neither this project nor its contributors are affiliated with or endorsed by VSCO or its services.

It is your responsibility to obtain copyright permission from users before downloading or reproducing copyrighted material. Failing to do so is a violation of copyright law.

## Installation
```
pip install vsco-download
```
## Sample Usage
Make sure you add a delay between requests otherwise you will get rate limited.
```python
from vsco_download.api import VscoApi
from time import sleep

username = 'sample username'

api = VscoApi()
side_id = api.get_site_id(username)
for medias in api.get_media_cursor(site_id):
    for media in medias:
        with open(f'output/{media.timestamp}{'.jpg' if media.is_image else '.mp4'}', 'wb') as file:
            media.download_to(file)
            sleep(5)
```
