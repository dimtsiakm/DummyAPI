import requests
import re
from datetime import date
from dateutil import parser
import validators

class Post:
    def __init__(self, json):
        self.id = str(json['id'])
        self.text = str(json['text'])
        self.image = str(json['image'])
        self.likes = int(json['likes'])
        self.link = str(json['link'])
        self.tags = list(json['tags'])
        self.publishDate = str(json['publishDate'])
        self.owner = json['owner']['id']

    def validate(self):
        if not validators.length(self.text, min=6, max=1000):
            print('Post - ', self.id, ', does not have validated text field')
            return False
        elif not validators.url(self.image):
            print('Post - ', self.id, ', does not have validated url')
            return False
        elif self.likes < 0:
            print('Post - ', self.id, ', does not have validated likes')
            return False
        elif not validators.url(self.link) and not validators.length(self.link, min=6, max=200):
            print('Post - ', self.id, ', does not have validated link')
            return False
        elif not isinstance(self.tags, list):
            print('Post - ', self.id, ', does not have validated tags')
            return False
        else:
            return True
        
    def is_dublicate(self, posts_list):
        for post in posts_list:
            if post.id == self.id:
                print('There is a same object')
                return True
        return False

    def check_if_user_exist(self, users):
        for u in users:
            if self.owner == u.id:
                return True
        print('Post id: - ', self.id, ', User does not exist')
        return False

    def get_full_posts(psts, users):
        headers = {'app-id': '6240aa8892ac1b1186be8d15'}
        posts = []
        print('posts processing..')
        for post in psts:
            url = 'https://dummyapi.io/data/v1/post/' + post['id']
            r = requests.get(url, headers=headers)
            post = Post(r.json())
            if post.validate() and not post.is_dublicate(posts) and post.check_if_user_exist(users):
                posts.append(post)
        return posts

