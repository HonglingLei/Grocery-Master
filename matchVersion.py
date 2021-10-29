"""
Name : pre_process.py
Author  : Hongliang Liu, Jing Li, Hongling Lei, Aishwarya Kura
Contact : honglian@andrew.cmu.edu
Time    : 2021/9/11 15:57
Desc: used to scrape data from website A
"""
import os
import re
import winreg
import zipfile
import requests

base_url = 'http://npm.taobao.org/mirrors/chromedriver/'
version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # Use reg to match the version of chrome


def getChromeVersion():
    """get Chrome Version"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Google\\Chrome\\BLBeacon')
        value, t = winreg.QueryValueEx(key, 'version')
        return version_re.findall(value)[0]  # return  3-bits version
    except WindowsError as e:
        # if not Chrome
        return "1.1.1"


def getChromeDriverVersion():
    """Search Chromedriver Version"""
    try:
        outstd2 = os.popen('chromedriver --version').read()
        version = outstd2.split(' ')[1]
        version = ".".join(version.split(".")[:-1])
        return version
    except Exception as e:
        return "0.0.0"


def getLatestChromeDriver(version):
    # Get the latest version of ChromeDriver
    url = f"{base_url}LATEST_RELEASE_{version}"
    latest_version = requests.get(url).text
    # Download...
    download_url = f"{base_url}{latest_version}/chromedriver_win32.zip"
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:  # save the ZIP in local file
        zip_file.write(file.content)
        zip_file.close()
   
    # UnZip
    f = zipfile.ZipFile("chromedriver.zip", 'r')
    for file in f.namelist():
        f.extract(file)
        f.close()
        os.remove("chromedriver.zip")
        return True 


def checkChromeDriverUpdate():
    chrome_version = getChromeVersion() #current chrome version
    driver_version = getChromeDriverVersion() #driver version
    print(chrome_version, driver_version)
    if chrome_version == driver_version:
        return True
    try:
        getLatestChromeDriver(chrome_version)
        return True
    except requests.exceptions.Timeout:
        #Timeout
        return False
    except Exception as e:
        print("Unknow exception: {}".format(e))
        return False
