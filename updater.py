import requests
from bs4 import BeautifulSoup
import re
import os
import csv

def contains_chara_info(data):
    aux = data.find_all('h3')
    if len(aux) > 0 and aux[0].text == 'NO DATA':
        return False
    return True


def get_HTML_from_url(url):
    page = requests.get(url)
    page = BeautifulSoup(page.content, "html.parser")
    return page


def check_for_bracket(word):
    if word[0] == '[':
        return word[0]+word[1:].capitalize()
    else:
        return word.capitalize()


def parse_name(name):
    return re.sub(' {2,}', ' ', name.split('\n')[1].strip())


def get_chara_id(data):
    return int(data.find_all('div', class_="glob__desc_type")[-1].text.strip().split(' ')[-1])


def save_chara_pic(picUrl):
    if not os.path.exists('./pics'):
        os.mkdir('./pics')
    filename = picUrl.split('/')[-1]
    r = requests.get(picUrl,stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open('./pics/'+filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return './pics/'+filename


def get_chara_pic(data):
    picSrc = data.find_all('div', class_="glob_artwork")[0].find_all('img')[0]['src']
    picUrl = 'https://saomd.fanadata.com/' + picSrc
    return save_chara_pic(picUrl)


def fix_name(name):
    old = name.split(' ')
    if len(old) == 1:
        return check_for_bracket(name) if len(name) > 0 else name
    fixedName = []
    fixedName.append(check_for_bracket(old[0]))
    for word in old[1:]:
        word = word.replace('’', "'")
        if word.lower() in ['of', 'the', 'a']:
            fixedName.append(word.lower())
        elif '-' in word:
            fixedName.append('-'.join([x.capitalize()
                             for x in word.split('-')]))
        else:
            fixedName.append(word.capitalize())
    return ' '.join(fixedName)


def get_chara_stuff(data):
    result = data.find_all('div', class_="title__first")
    name = parse_name(result[0].find_all('h5')[0].text)
    name = fix_name(name)
    unitName = result[0].find_all('h6')[0].text.lower().strip()
    unitName = fix_name(unitName).replace('’', "'")
    return name, unitName, ' '.join([unitName,name])

def make_CSV(charaList):
    with open('charaInfo.csv', 'w', encoding='UTF8',newline='') as f:
        writer = csv.writer(f,delimiter=';')
        writer.writerow(['Id','CharaName','UnitName','FullName','picPath'])
        writer.writerows(charaList)

def get_all_charas():
    baseUrl = 'https://saomd.fanadata.com/character-'
    charaList = []
    num = 1
    while num < 1600:
        data = get_HTML_from_url(f'{baseUrl}{num}')
        if contains_chara_info(data):
            print(f'{baseUrl}{num}')
            info = []
            info.append(get_chara_id(data))
            info.extend(get_chara_stuff(data))
            info.append(get_chara_pic(data))
            charaList.append(info)
        num += 1
    charaList = sorted(charaList,key=lambda x:x[0])
    make_CSV(charaList)
if __name__ == '__main__':
    get_all_charas()
