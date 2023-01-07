#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2023 jwalkiew
# Author: jwalkiew

import os
import sys
import time

from selenium.webdriver.common.by import By
from seleniumwire import webdriver

ROOT_DIRECTORY = '/opt/kwscanner/'
ROOT_KW_DIRECTORY = '%sout/kw/' % ROOT_DIRECTORY
ROOT_LOG_DIRECTORY = '%sout/log/' % ROOT_DIRECTORY
FILENAME_FOUND = 'kw-found.txt'
FILENAME_NOT_FOUND = 'kw-not-found.txt'
FILENAME_UNAVAILABLE = 'kw-unavailable.txt'
FILENAME_UNKNOWN_ERROR = 'kw-unknown-error.txt'

MAX_TRIES_PER_NUMBER = 3


def get_kw_number(number):
    values = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'X': 10, 'A': 11, 'B': 12,
        'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20, 'K': 21, 'L': 22, 'M': 23, 'N': 24,
        'O': 25, 'P': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'W': 31, 'Y': 32, 'Z': 33,
    }
    weights = [1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]
    result = 0
    for idx in range(0, len(number)):
        result = result + values[number[idx]] * weights[idx]
    control_digit = result % 10
    return '%s/%s/%s' % (number[0:4], number[4:], control_digit)


def get_total_kw_number(code, number):
    return get_kw_number('%s%s' % (code, f'{number:08}'))


def save_file(file_name, content):
    with open("%s" % file_name, 'w') as f:
        f.write(content)


def append_file(file_name, content):
    with open("%s" % file_name, 'a') as f:
        f.write(content)


def interceptor(request):
    request.headers['accept-language'] = 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Run:')
        print('$ python kwscanner.py <CODE> <BEGIN> <END>')
        print('example:')
        print('$ python kwscanner.py SI1G 0 8000')
        exit(0)
    os.makedirs(ROOT_KW_DIRECTORY, exist_ok=True)
    os.makedirs(ROOT_LOG_DIRECTORY, exist_ok=True)
    kw_code = sys.argv[1]
    begin = int(sys.argv[2])
    end = int(sys.argv[3])
    kw_numbers = range(begin, end)
    not_found_list = []
    unavailable_list = []
    unknown_error_list = []
    for i in kw_numbers:
        kw_number = get_total_kw_number(kw_code, i)
        kw_number_parts = kw_number.split('/')
        file_name_part = '%s_%s_%s' % (kw_number_parts[0], kw_number_parts[1], kw_number_parts[2])
        driver = None
        print('%s (%s)' % (kw_number, i))

        iteration = 0
        successful = False
        while not successful:
            if iteration == MAX_TRIES_PER_NUMBER:
                break
            iteration = iteration + 1
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
                driver = webdriver.Chrome(executable_path='%schromedriver' % ROOT_DIRECTORY, options=chrome_options)
                driver.request_interceptor = interceptor

                driver.get("https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW")
                time.sleep(5)

                driver.find_element(By.ID, "kodWydzialuInput").click()
                driver.find_element(By.ID, "kodWydzialuInput").send_keys("%s" % kw_number_parts[0])
                driver.find_element(By.ID, "numerKsiegiWieczystej").click()
                driver.find_element(By.ID, "numerKsiegiWieczystej").send_keys("%s" % kw_number_parts[1])
                driver.find_element(By.ID, "cyfraKontrolna").click()
                driver.find_element(By.ID, "cyfraKontrolna").send_keys("%s" % kw_number_parts[2])
                time.sleep(1)

                driver.find_element(By.ID, "wyszukaj").click()
                time.sleep(2)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                driver.find_element(By.ID, "przyciskWydrukZwykly").click()
                time.sleep(1)

                driver.find_element(By.CSS_SELECTOR, "h2 > b").click()
                t_i_o = driver.page_source
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "td:nth-child(2) input:nth-child(7)").click()
                t_i_sp = driver.page_source
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "td:nth-child(3) input:nth-child(7)").click()
                t_ii = driver.page_source
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "td:nth-child(4) input:nth-child(7)").click()
                t_iii = driver.page_source
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "td:nth-child(5) input:nth-child(7)").click()
                t_iv = driver.page_source
                time.sleep(1)
                save_file("%s%s__1__I-O.html" % (ROOT_KW_DIRECTORY, file_name_part), t_i_o)
                save_file("%s%s__2__I-SP.html" % (ROOT_KW_DIRECTORY, file_name_part), t_i_sp)
                save_file("%s%s__3__II.html" % (ROOT_KW_DIRECTORY, file_name_part), t_ii)
                save_file("%s%s__4__III.html" % (ROOT_KW_DIRECTORY, file_name_part), t_iii)
                save_file("%s%s__5__IV.html" % (ROOT_KW_DIRECTORY, file_name_part), t_iv)
                append_file('%s%s' % (ROOT_LOG_DIRECTORY, FILENAME_FOUND), '%s\n' % kw_number)
                successful = True
            except:
                if 'nie została odnaleziona' in driver.page_source:
                    successful = True
                    not_found_list.append(kw_number)
                    append_file('%s%s' % (ROOT_LOG_DIRECTORY, FILENAME_NOT_FOUND), '%s\n' % kw_number)
                    print('Not found... continue')
                elif '<button name="przyciskWydrukZwyklyDisabled" id="przyciskWydrukZwyklyDisabled" class="left light-blue-gradient" disabled="disabled">' in driver.page_source:
                    successful = True
                    unavailable_list.append(kw_number)
                    append_file('%s%s' % (ROOT_LOG_DIRECTORY, FILENAME_UNAVAILABLE), '%s\n' % kw_number)
                    print('Unavailable')
                elif '<title>Request Rejected</title>' in driver.page_source:
                    timeToSleepInSeconds = 10
                    print('Wait for %d seconds...' % timeToSleepInSeconds)
                    time.sleep(timeToSleepInSeconds)
                    print('and try again...')
                else:
                    successful = True
                    unknown_error_list.append(kw_number)
                    append_file('%s%s' % (ROOT_LOG_DIRECTORY, FILENAME_UNKNOWN_ERROR), '%s\n' % kw_number)
                    print('Unknown error')
                    print(sys.exc_info())
            if driver is not None:
                driver.close()
                driver.quit()
            time.sleep(1)
    print('not_found_list')
    print(not_found_list)
    print('unavailable_list')
    print(unavailable_list)
    print('unknown_error_list')
    print(unknown_error_list)
    print('found')
    print(len(kw_numbers) - len(not_found_list) - len(unavailable_list) - len(unknown_error_list))
