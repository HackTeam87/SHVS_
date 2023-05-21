#!/usr/bin/env python3
import os
import yaml
import voice
import webbrowser
from telnetlib import Telnet
import subprocess
import requests as r

def load_file(filename):
    with open(filename, encoding='utf-8') as f: 
        file = yaml.safe_load(f) 
        return file
    

#id=20,21,26
def led_on(*query):
    link = 'http://172.16.1.19:5000/'
    data = {'Relay': 21}
    headers = {'Content-type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain'}
    r.post(link, data=data, headers=headers)            

def ssh_connect(*query):
		print('Enter your host: ')
		host = input()
		os.system(f'ssh -i configs\id_rsa grin@{host}')


def show_list_device(*query):
    test = load_file('configs/device_list.yaml')
    for t in test:
        print(f'ключ: {t}\n значение: {test[t]}')


def browser(*query):
	query = ' '.join(query)
	webbrowser.open(f'http://www.google.com/search?q={query}')

def passive(*query):
		'''Функция заглушка при простом диалоге с ботом'''
		pass        
	
