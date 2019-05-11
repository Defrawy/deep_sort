# from urllib2 import urlopen, URLError, HTTPError
from urllib.parse import urlparse
from urllib.request import urlretrieve, urlopen, build_opener, install_opener, URLopener, HTTPCookieProcessor
from console_progressbar import ProgressBar
from os.path import splitext, basename
from bs4 import BeautifulSoup

import os
import zipfile
import json
import sys
import shutil
# import urlib

def download_progress(t_blocks, block_size, file_size):
    if file_size < 0:
        file_size = ((t_blocks + 1) * block_size)

    pb.print_progress_bar((t_blocks * block_size) / file_size * 100)


def unzipfile(file):
    try:
        zip_ref = zipfile.ZipFile(file, 'r')
        # make directory with file name
        # os.mkdir(file.split('.')[0])
        zip_ref.extractall("./")
        zip_ref.close()   
    except Exception as e:
        pass  
    

def parse_page(link):
    if 'mediafire' not in link:
        return link

    response = urlopen(link).read()
    h = BeautifulSoup(response, 'html.parser').find('a', attrs={'class': 'input', 'aria-label': 'Download file'}).get('href')
    return h

def download_file(bn, url, filename):
    if not config["force_download"]:
        return

    download_link = parse_page(url)
    url_components = urlparse(download_link)    
    
    name, file_ext = splitext(basename(url_components.path))
    file_path = os.path.join(os.getcwd(), bn + name + file_ext)
    exists = os.path.isfile(file_path)
    if exists:
        pass
    else:
        # opener.retrieve(url, file_path, download_progress)
        urlretrieve(download_link, file_path, download_progress)
    
    print("\nDownload Complete\n")
    if file_ext == '.zip':
        check_folder_exits(name, file_ext)
        # print("\nUnzipping file...\n")
        # unzipfile(filename)
        # print("\nUnzipping Complete\n")

    rmv_MACOSX()


def rmv_MACOSX():
    if os.path.exists("__MACOSX"):
        shutil.rmtree("__MACOSX", ignore_errors=True, onerror=None)

    if os.path.exists(".DS_Store"):
        os.remove(".DS_Store")

    # os.makedirs(target_folder)


def check_folder_exits(name, file_ext):
    print("\nUnzipping file...\n")
    # cancel unzipping
    if config["force_unzipping"]:
        unzipfile(name+file_ext)
    
    if not os.path.exists(os.path.join(os.getcwd(), name)):
        unzipfile(name+file_ext)
    print("\nUnzipping Complete\n")


# first load the config file 
with open('app.config') as data:
    config = json.load(data)

# os.path.join(os.getcwd(), basename + filename)
items = [(config["res_struct"]["networks"], "mars-small128.ckpt-68577", "http://www.mediafire.com/file/i8ulgnq050k8c9v/mars-small128.ckpt-68577/file"), 
    (config["res_struct"]["networks"], "mars-small128.ckpt-68577.meta", "http://www.mediafire.com/file/m7eciqc1q4ipi5v/mars-small128.ckpt-68577.meta/file"), 
    (config["res_struct"]["networks"], "mars-small128.pb", "http://www.mediafire.com/file/lch8dhv54obckb2/mars-small128.pb/file"), 
    ("./", "MOT16.zip", "https://motchallenge.net/data/MOT16.zip")]


# opener = URLopener()
# this fix 302 error 
opener = build_opener(HTTPCookieProcessor())
install_opener(opener)
pb = ProgressBar(total=100,prefix='Here', suffix='Now', decimals=3, length=50, fill='X', zfill='-')



LEFT_STR = '\n=========================================\n\t'
RGHT_STR = '\n=========================================\n'

if not os.path.exists(config["res_struct"]["networks"]):
    os.makedirs(config["res_struct"]["networks"])

if not os.path.exists(config["res_struct"]["output_dir"]):
    os.makedirs(config["res_struct"]["output_dir"])

if not os.path.exists(config["res_struct"]["output_rec"]):
    os.makedirs(config["res_struct"]["output_rec"])


os.system("clear")
os.system("echo '{}Downloading Requried Files....{}'".format(LEFT_STR, RGHT_STR))
for (bn, filename, url) in items:
    try:
        download_file(bn, url, filename)
    except Exception as e:
        print(e)
        


if config["mode"] != "online" and not os.path.exists(config["detection_file"]):
    os.system("clear")
    os.system("echo '{}Build Detection....{}'".format(LEFT_STR, RGHT_STR))
    os.system('python build_npy.py')

if config["play_demo"]:
    os.system("clear")
    os.system("echo '{}Running Demo....{}'".format(LEFT_STR, RGHT_STR))
    os.system('python run.py')

config["play_demo"] = False
config["force_download"] = False 
config["force_unzipping"] = False

with open('app.config', 'w') as outfile:
    json.dump(config, outfile)

    

