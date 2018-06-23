import requests
import os
import shutil
from bs4 import BeautifulSoup

FILE_TYPES = ('gif', 'jpg', 'jpeg', 'mp4', 'png', 'gifv', 'webm')


def check_path(url_):
    folder_name = url_.split('/')[-1].split('.html')[0]
    if os.path.exists(folder_name):
        os.chdir(folder_name)
    else:
        os.mkdir(folder_name)
        os.chdir(folder_name)
    print("Downloading to folder: {}".format(folder_name))


class Image(object):
    def __init__(self, file_url):
        self.file_url = file_url
        self.file_name = self.file_url.split('/')[-1]
        self.file_data = requests.get(self.file_url, stream=True)

    def download(self):
        print("Downloading: {}".format(self.file_url))
        with open(self.file_name, 'wb') as f:
            shutil.copyfileobj(self.file_data.raw, f)


if __name__ == '__main__':
    try:
        url = input("Enter url: ")
        check_path(url)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        for link in soup.find_all('a'):
            href = str(link.get('href'))
            for i in FILE_TYPES:
                if i in href:
                    if 'player' not in href:
                        file_i = Image(href)
                        file_i.download()
                    else:
                        continue
    except KeyboardInterrupt:
        print("Downloading cancelled!")

