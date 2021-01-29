from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import multiprocessing
import requests
import urllib
import os


def get_continents():
    page = requests.get(f'https://dds.cr.usgs.gov/srtm/version2_1/SRTM3')
    soup = BeautifulSoup(page.content, features='html.parser')
    links = soup.findAll('a')
    folders = [x.text.replace('/', '').strip() for x in links]
    # Removes 'Parent Directory'
    folders.pop(0)
    return folders


def get_file_names(folder):
    page = requests.get(f'https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/{folder}/')
    soup = BeautifulSoup(page.content, features='html.parser')
    file_names = [a['href'] for a in soup.findAll('a')]
    # Removes 'Parent Directory'
    file_names.pop(0)
    return file_names


def download(folder, file_name):
    t = urllib.request.URLopener()
    t.retrieve(f"https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/{folder}/{file_name}", f"downloaded_data/{file_name}")
    print(f'Downloaded: {file_name} ({folder})')


# Creating the folder where the downloads will be stored
if not os.path.exists('downloaded_data'):
    os.makedirs('downloaded_data')

continents = get_continents()
num_cores = multiprocessing.cpu_count()
for c in continents:
    files = get_file_names(c)
    Parallel(n_jobs=num_cores)(delayed(download)(c, fn) for fn in files)
