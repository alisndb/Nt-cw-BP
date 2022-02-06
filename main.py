from handlers import VKontakte, YandexDisk
import time
import datetime
import json
from progress.bar import IncrementalBar


class PhotoUploader:
    def __init__(self, vk, yd, owner_id=None, album_id='profile'):  # album_id='profile'/'wall'
        self.vk = vk
        self.yd = yd
        self.owner_id = owner_id
        self.album_id = album_id

    def _get_photos(self):
        res = self.vk.get_photos(self.owner_id, self.album_id)
        items_params = []
        for item in res['response']['items']:
            item_params = {
                'url': item['sizes'][-1]['url'],
                'size': item['sizes'][-1]['type'],
                'file_name': f"{item['likes']['count']}.jpg",
                'date': item['date']
            }
            items_params.append(item_params)
        files_names = [item['file_name'] for item in items_params]
        for item in items_params:
            if files_names.count(item['file_name']) > 1:
                files_names.remove(item['file_name'])
                date = datetime.datetime.fromtimestamp(item['date'])
                item['file_name'] = f"{item['file_name'][:-4]}_{date.strftime('%d-%m-%Y')}.jpg"
            del item['date']
        self.items_params = items_params

    def _upload_photos(self):
        bar = IncrementalBar('Загрузка...', max=len(self.items_params)+2)
        folder = f'photos-vk-{self.album_id}'
        self.yd.delete_object(folder)
        bar.next()
        time.sleep(3)
        self.yd.create_folder(folder)
        bar.next()
        time.sleep(0.3)
        for item in self.items_params:
            self.yd.upload_file_to_disk(f"{folder}/{item['file_name']}", item['url'])
            time.sleep(0.03)
            del item['url']
            bar.next()
        if self.album_id == 'profile':
            with open('photos-vk-profile.json', 'w') as file:
                json.dump(self.items_params, file, indent=2)
        else:
            with open('photos-vk-wall.json', 'w') as file:
                json.dump(self.items_params, file, indent=2)
        bar.finish()

    def get_and_upload_photos(self):
        print('Получение фото из ВКонтакте...')
        self._get_photos()
        print('Загрузка фото на Яндекс.Диск...')
        self._upload_photos()
        print('Фото успешно загружены!')


vk_token = ''  # Токен ВКонтакте
yd_token = ''  # Токен Яндекс.Диска

vk_client = VKontakte.VKontakte(vk_token, '5.131')
yd_client = YandexDisk.YandexDisk(yd_token)
photo_uploader = PhotoUploader(vk=vk_client, yd=yd_client, album_id='profile')  # album_id='profile'/'wall'

photo_uploader.get_and_upload_photos()
