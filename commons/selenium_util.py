# -*- coding: utf-8 -*-

import traceback
import time
import platform
from selenium import webdriver


def check_server():
    return platform.system() != 'Darwin'


def get_driver(driver_type='chrome', download_path=''):
    chrome_executable_path = '/usr/local/bin/chromedriver'

    try:
        if driver_type == 'headless-chrome':
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-urlfetcher-cert-requests")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1280,1024")

            options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'

            if download_path != '':
                options.add_experimental_option("prefs", {
                    "download.default_directory": download_path,
                    "download.directory_upgrade": True,
                })

            return webdriver.Chrome(executable_path=chrome_executable_path, chrome_options=options)
        elif driver_type == 'phantomjs':
            return webdriver.PhantomJS()
        elif driver_type == 'firefox':
            return webdriver.Firefox('/usr/local/bin/geckodriver')
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-urlfetcher-cert-requests")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1280,1024")

            if download_path != '':
                logger.debug('set download path = %s' % download_path)
                options.add_experimental_option("prefs", {
                    "download.default_directory": download_path,
                    "download.directory_upgrade": True,
                })

            return webdriver.Chrome(executable_path=chrome_executable_path, chrome_options=options)
    except Exception:
        traceback.print_exc()


def retry_n(retry_count, sleep_time, func, *args):
    for i in range(retry_count):
        if func(*args):
            return

        print('retry!!! sleep %d' % sleep_time)
        time.sleep(sleep_time)


def check_page(driver, url):
    print('req=%s, current=%s' % (url, driver.current_url))

    if driver.current_url == url:
        return True

    return False
