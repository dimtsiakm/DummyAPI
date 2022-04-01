import requests
from datetime import date
from dateutil import parser
import validators

class Comment:
    def __init__(self, json):
        self.id = str(json['id'])
        self.message = str(json['message'])
        self.owner = str(json['owner']['id'])
        self.post = str(json['post'])
        self.publishDate = str(json['publishDate'])

    def validate(self):
        if not validators.length(self.message, min=2, max=500):
            print('Comment - ', self.id, ', does not have validated text field')
            return False
        else:
            return True
        
    def is_dublicate(self, comment_list):
        for comm in comment_list:
            if comm.id == self.id:
                print('There is a same object')
                return True
        return False

    def check_if_user_exist(self, users):
        for u in users:
            if self.owner == u.id:
                return True
        print('Comment id: - ', self.id, ', User does not exist')
        return False

    def check_if_post_exist(self, posts):
        for p in posts:
            if self.post == p.id:
                return True
        print('Comment id: - ', self.id, ', Post does not exist')
        return False

    def get_comments(url_base, users, posts):
        page = 0
        limit = 50
        print(url_base)
        headers = {'app-id': '6240aa8892ac1b1186be8d15'}
        comments = []

        while True:
            url = url_base + str(page) + '&limit=' + str(limit)
            r = requests.get(url, headers=headers)
            print('page', page)
            if len(r.json()['data']) == 0:
                return comments
            for json_comment in r.json()['data']:
                comment = Comment(json_comment)
                if comment.validate() and not comment.is_dublicate(posts) and comment.check_if_user_exist(users) and comment.check_if_post_exist(posts):
                    comments.append(comment)
            page += 1
