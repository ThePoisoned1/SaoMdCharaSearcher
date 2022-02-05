import csv
import os
import updater
import argparse
import cv2
from pprint import pprint


def load_CSV(path):
    with open(path, 'r+', newline='', encoding="utf8") as file:
        reader = csv.reader(file, delimiter=';')
        res = list(map(tuple, reader))
    return res[1:]


def get_search_results(search, data):
    search = search.lower()
    results = []
    for entry in data:
        if any(search in value.lower().strip() for value in entry):
            results.append(entry)
        if entry[3].strip().lower() == search:
            return [entry]
    return results


def show_image(path, title='Image'):
    print(path)
    if not os.path.exists(path):
        print('Image path not found, u may need a chara update')
    cv2.imshow(title, cv2.imread(path))
    cv2.waitKey(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Searches for SAOMD characters')
    parser.add_argument('search', type=str, nargs=1, help='Stuff to search')
    parser.add_argument('--update', '-u', action='store_true',
                        help='Runs a character update')
    args = parser.parse_args()
    csvPath = 'charaInfo.csv'
    if args.update and os.path.exists(csvPath):
        os.remove(csvPath)
    if not os.path.exists(csvPath):
        print('No csv found, downloading all the charas')
        updater.get_all_charas()
    data = load_CSV(csvPath)
    results = get_search_results(args.search[0], data)
    if len(results) == 1:
        print(results[0])
        show_image(results[0][-1], title=f'({results[0][0]}) {results[0][3]}')
    elif len(results) == 0:
        print('Nothing found')
    else:
        if len(results) < 11:
            [print(result) for result in results]
        else:
            print('Way to many results for that')
