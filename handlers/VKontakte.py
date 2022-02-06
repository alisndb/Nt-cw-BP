import requests


class VKontakte:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self, owner_id=None, album_id='profile'):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': 1
        }
        res = requests.get(get_photos_url, params={**self.params, **get_photos_params})
        if res.status_code != 200:
            return f'Ошибка: {res.status_code}'
        return res.json()
