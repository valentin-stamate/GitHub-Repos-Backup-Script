import os
import re
import shutil

import requests


repo_name_regex = re.compile(f'([/])([^/]+)([.]git)$')


def get_repos_url(username):
    link = (f'https://api.github.com/users/{username}/repos')

    api_link = requests.get(link)
    api_data = api_link.json()

    repos_data = (api_data)

    repos_name = []

    [repos_name.append(items['name']) for items in repos_data]

    full_repos_url = []
    for i in range(len(repos_name)):
        full_repos_url.append(f'https://github.com/{username}/{repos_name[i]}.git')

    return full_repos_url


def get_repo_name(url):
    return repo_name_regex.findall(url)[0][1]


def put_list_in_file(_list, path, file_name):
    with open(os.path.join(path, file_name), 'w') as f:
        for x in _list:
            f.write(f'{x}\n')
        f.flush()


def read_file_lines(path):
    _list = []

    with open(path, 'r') as f:
        for line in f.readlines():
            _list.append(line.rstrip('\n'))

    return _list


def clone(repo_list):
    folder = 'repos'

    for i in range(len(repo_list)):
        url = repo_list[i]
        os.system(f'git clone {url} {folder}/{get_repo_name(url)}')


def main():
    path = 'list'
    username = 'StamateValentin'

    put_list_in_file(get_repos_url(username), path, 'public')

    public_list = read_file_lines(os.path.join(path, 'public'))    # public repos from your account
    private_list = read_file_lines(os.path.join(path, 'private'))  # private repos the you could put manually

    public_list.extend(private_list)
    full_list = public_list

    clone(full_list)


if __name__ == '__main__':
    main()

