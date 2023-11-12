import requests
from io import BytesIO
import yadisk
import json
from tkinter import *
from tkinter.ttk import *
import time


def write_json(data, name_json):
    with open(f'{name_json}', 'w') as file:
        json.dump(data,file, indent=2, ensure_ascii=False)

def get_largest(size_dick):
    return size_dick['height']

def count_file_name(count_name_list):
    for first in count_name_list:
        name_file = first['mane']
        i = 0
        for second in count_name_list:
            name_count = second['mane']
            if name_file == name_count:
                i +=1
                if i >= 2:
                    first['mane'] = str(first['mane']) + '_' + str(first['date'])
                    second['mane'] = str(second['mane']) + '_' + str(second['date'])
    return count_name_list

def start(owner_id, token_YA, folder_name):
    return owner_id, token_YA, folder_name

def start_download():
    start(owner_id, token_YA, folder_name)
    params = {
        'owner_id': owner_id,
        'access_token': '??????????????????????????????',
        'v': '5.131',
        'album_id': 'profile',
        'extended': True,
        'photo_sizes': True
    }
    r = requests.get('https://api.vk.com/method/photos.get', params=params)
    write_json((r.json()), 'photos.json')

    photos = json.load(open('photos.json'))['response']['items']
    file_list = []

    for photo in photos:
        sizes = photo['sizes']
        file_name = photo['likes']['count']
        date_file = photo['date']

        max_size_url = max(sizes, key=get_largest)['url']
        max_size_type = max(sizes, key=get_largest)['type']
        max_size_pic = max(sizes, key=get_largest)['height'] * max(sizes, key=get_largest)['width']

        file_dict = {'mane': file_name, 'url': max_size_url, 'date': date_file, 'type': max_size_type, 'pixels': max_size_pic}
        file_list.append(file_dict)

    file_list_sort = sorted(file_list, key=lambda d: d['pixels'], reverse=True)

    # Сохранять указанное количество фотографий(по умолчанию 5) наибольшего
    # размера(ширина / высота в пикселях) на Я.Диске

    final_files = count_file_name(file_list_sort[:5])

    VK_download_YA(final_files, token_YA, folder_name)

def VK_download_YA(final_files, token_YA, folder_name):

    data = []

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth {token_YA}'
    }

    # Для загруженных фотографий нужно создать свою папку.
    create_a_folder = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                   params={'path': f'Загрузки/{folder_name}'}, headers=headers)


    VK_files = len(final_files)
    download = 0
    speed = 1

    for file in final_files:

        time.sleep(0)
        bar['value'] += (speed / VK_files) * 100
        download += speed
        percent.set(str(int((download / VK_files) * 100)) + "%")
        text.set(str(download) + "/" + str(VK_files) + " Download completed")
        window.update_idletasks()

        file_name = file['mane']
        file_url = file['url']
        file_type = file['type']
        data.append({'file_name': f'{file_name}.jpg', 'size': file_type})
        with requests.get(file_url, stream=True) as r:
            if r.status_code != 200:
                print("Ошибка при получении файла")
                exit()
            file_data = BytesIO(r.content)
            y = yadisk.YaDisk(token = token_YA)
            y.upload(file_data, f'/Загрузки/{folder_name}/{file_name}.jpg')
        if download == VK_files:
            write_json(data, 'information_on_uploaded_files.json')
            exit()


if __name__ == '__main__':
    # id пользователя vk
    owner_id = ???????????
    # токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!
    token_YA = ??????????????????

    folder_name = 'PhotoVK'
    start(owner_id, token_YA, folder_name)

    window = Tk()
    percent = StringVar()
    text = StringVar()

    bar = Progressbar(window, orient=HORIZONTAL, length=500)
    bar.pack(pady=10)

    percentLabel = Label(window, textvariable=percent).pack()
    taskLabel = Label(window, textvariable=text).pack()
    button = Button(window, text='Start download Photos VK in YA_Disk', command=start_download).pack()
    window.mainloop()












