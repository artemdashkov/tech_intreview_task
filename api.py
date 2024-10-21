import time
from datetime import datetime

import pytest
import requests
from src import CloudYandex, DogCeo


class YaUploader:
    def __init__(self):
        self.__token = 'AgAAAAAJtest_tokenxkUEdew' # this token doesn't work. i uses own token.

    def create_folder(self, name_folder):
        print(f"\n{datetime.now()}\t Start to create folder: '{name_folder}'.")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.__token}'}
        response = requests.put(f'{CloudYandex.BASE_URL}?path={name_folder}', headers=headers)
        if 200 or 201 in response.status_code:
            print(f"{datetime.now()}\t Folder: '{CloudYandex.BASE_URL}?path={name_folder}' was created.")
        else:
            msg = f"{datetime.now()}\t Current status_code is {response.status_code}. Need to fix problem."
            pytest.fail(msg)

    def upload_photos_to_yd(self, name_folder, url_for_download, name_file):
        print(f"\n{datetime.now()}\t Start to upload: '{name_file}'.")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.__token}'}
        params = {"path": f'/{name_folder}/{name_file}', 'url': url_for_download, "overwrite": "true"}
        response = requests.post(CloudYandex.UPLOAD_URL, headers=headers, params=params)
        time.sleep(5)
        if 200 or 202 in response.status_code:
            print(f"{datetime.now()}\t End to upload: '{name_file}'.")
        else:
            msg = f"{datetime.now()}\t Current status_code is {response.status_code}. Need to fix problem."
            pytest.fail(msg)

    def get_response(self, name_folder):
        print(f"\n{datetime.now()}\t Start to get response.")
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   # 'Authorization': f'OAuth AgAAAAAJtest_tokenxkUEdew',
                   'Authorization': self.__token}
        response = requests.get(f'{CloudYandex.BASE_URL}?path=/{name_folder}', headers=headers)
        if response.status_code == 200:
            print(f"{datetime.now()}\t End to get response.")
            return response
        else:
            msg = f"{datetime.now()}\t Current status_code is {response.status_code}. Need to fix problem."
            pytest.fail(msg)

    def delete_folder(self, name_folder):
        print(f"\n{datetime.now()}\t Start to delete folder: '{name_folder}'.")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.__token}'}
        params = {"path": f'/{name_folder}', "permanently": "true"}
        response = requests.delete(f'{CloudYandex.BASE_URL}?path={name_folder}', params=params, headers=headers)
        if 200 or 202 or 204 in response.status_code:
            print(f"{datetime.now()}\t Folder: '{CloudYandex.BASE_URL}?path={name_folder}' was delete.")
        else:
            msg = f"{datetime.now()}\t Current status_code is {response.status_code}. Need to fix problem."
            pytest.fail(msg)



def get_sub_breeds(breed):
    print(f"\n{datetime.now()}\t Start to get sub breeds for: '{breed}'.")
    response = requests.get(f'{DogCeo.BASE_URL}/{breed}/list')
    if response.status_code == 200:
        print(f"{datetime.now()}\t Sub breeds were received. List of sub breeds is: '{response.json()['message']}'.")
        return response.json()['message']
    else:
        msg = f"{datetime.now()}\t Current status_code is {response.status_code}. Need to fix problem."
        pytest.fail(msg)


def get_urls(breed, sub_breeds):
    print(f"\n{datetime.now()}\t Start to get URLs for breed: '{breed}' and sub breeds: '{sub_breeds}'.")
    url_images = []
    if sub_breeds:
        for sub_breed in sub_breeds:
            response = requests.get(f"{DogCeo.BASE_URL}/{breed}/{sub_breed}/images/random")
            sub_breed_urls = response.json().get('message')
            print(f"{datetime.now()}\t Get URL for sub breeds: '{sub_breed_urls}'.")
            url_images.append(sub_breed_urls)
    else:
        response = requests.get(f"{DogCeo.BASE_URL}/{breed}/images/random")
        breed_url = response.json().get('message')
        print(f"{datetime.now()}\t Get URL for breed: '{breed_url}'.")
        url_images.append(breed_url)

    return url_images


def prepare_test_data(breed, name_folder):
    # Get sub breads
    sub_breeds = get_sub_breeds(breed)

    # Get urls to images
    urls = get_urls(breed, sub_breeds)

    # Create folder '/test_folder'
    yandex_client = YaUploader()
    yandex_client.create_folder(name_folder)

    for url in urls:
        part_name = url.split('/')
        name_file = '_'.join([part_name[-2], part_name[-1]])
        yandex_client.upload_photos_to_yd(name_folder, url, name_file)