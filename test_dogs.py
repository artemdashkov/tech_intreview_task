import random
from datetime import datetime

import pytest

from api import prepare_test_data, YaUploader, get_sub_breeds


@pytest.mark.parametrize('breed', ['doberman', random.choice(['bulldog', 'collie'])])
# @pytest.mark.parametrize('breed', ['doberman'])
def test_upload_dog(breed, clear):
    # start Arrange.
    prepare_test_data(breed, 'test_folder')

    # Start Act
    data_from_yd = YaUploader()
    response = data_from_yd.get_response('test_folder')

    # Start Assert
    assert response.json()['type'] == "dir", "The type of the created folder is not a 'dir'"
    print(f"{datetime.now()}\t The type of the created folder is a 'dir'")

    assert response.json()['name'] == "test_folder", "The name of the created folder is not a 'test_folder'"
    print(f"{datetime.now()}\t The name of the created folder is a 'test_folder'")

    for item in response.json()['_embedded']['items']:
        assert item['type'] == 'file', "The type of the file is not a 'file'"
        print(f"{datetime.now()}\t The type of the file is a 'file'")

        assert item['name'].startswith(breed), "The name of file not correspond breed"
        print(f"{datetime.now()}\t The name of file correspond breed")

    if get_sub_breeds(breed) == []:
        assert len(response.json()['_embedded']['items']) == 1, \
            "The numbers of files more then one or file missing"
        print(f"{datetime.now()}\t The numbers of files is one")

    else:
        assert len(response.json()['_embedded']['items']) == len(get_sub_breeds(breed)),\
            "The numbers of files not correspond numbers of sub breed"
        print(f"{datetime.now()}\t The numbers of files correspond numbers of sub breed")
