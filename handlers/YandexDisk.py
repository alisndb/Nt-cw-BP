import requests


class YandexDisk:
    url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token}'
        }

    def upload_file_to_disk(self, cloud_path, url):
        upload_url = self.url + 'resources/upload'
        params = {
            'path': cloud_path,
            'url': url
        }
        res = requests.post(upload_url, headers=self.headers, params=params)
        if res.status_code != 202:
            return f'Ошибка: {res.status_code}'
        return 'Файл успешно загружен!'

    def create_folder(self, cloud_path):
        resources_url = self.url + 'resources'
        params = {
            'path': cloud_path
        }
        res = requests.put(resources_url, headers=self.headers, params=params)
        if res.status_code != 201:
            return f'Ошибка: {res.status_code}'
        return 'Папка успешно создана!'

    def delete_object(self, cloud_path):
        resources_url = self.url + 'resources'
        params = {
            'path': cloud_path
        }
        res = requests.delete(resources_url, headers=self.headers, params=params)
        if res.status_code != 204:
            return f'Ошибка: {res.status_code}'
        return 'Объект успешно удален!'
