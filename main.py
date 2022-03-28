import requests
import json


class Comment:
    def __init__(self, id):
        self.id = id

    def print_currect_id(self):
        print(self.id)


class Post:
    def __init__(self, id):
        self.id = id

    def print_currect_id(self):
        print(self.id)


class User:
    def __init__(self, json):
        self.id = json['id']
        self.title = json['title']
        self.firstName = json['firstName']
        self.lastName = json['lastName']
        self.picture = json['picture']
        self.gender = json['gender']
        self.email = json['email']
        self.dateOfBirth = json['dateOfBirth']
        self.phone = json['phone']
        self.location = json['location']
        self.registerDate = json['registerDate']
        self.updatedDate = json['updatedDate']

    def print_currect_id(self):
        print(self.id)

headers = {'app-id': '6240aa8892ac1b1186be8d15'}

def fetch_data(url_base):
    page = 0
    limit = 50
    json_list = []
    print(url_base)
    while True:
        url = url_base + str(page) + '&limit=' + str(limit)
        r = requests.get(url, headers=headers)
        print('page', page)
        if len(r.json()['data']) == 0:
            return json_list
        json_list += r.json()['data']
        page += 1


def get_full_users(usrs):
    users = []
    for user in usrs:
        url = 'https://dummyapi.io/data/v1/user/' + user['id']
        r = requests.get(url, headers=headers)
        user = User(r.json())
        users.append(user)
    return users

if __name__ == '__main__':
    url_users = 'https://dummyapi.io/data/v1/user?page='
    url_posts = 'https://dummyapi.io/data/v1/post?page='
    url_comments = 'https://dummyapi.io/data/v1/comment?page='

    fetched_users = fetch_data(url_base=url_users)
    # fetched_posts = fetch_data(url_base=url_posts)
    # fetched_comments = fetch_data(url_base=url_comments)

    users = get_full_users(fetched_users)
    for u in users:
        u.print_currect_id()

    # print(len(fetched_comments))
    # print(len(fetched_comments))