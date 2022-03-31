import requests
from user import User as user
from post import Post as post
from comment import Comment as comment
from managerdb import *

def fetch_data(url_base):
    headers = {'app-id': '6240aa8892ac1b1186be8d15'}
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

"""main function"""
if __name__ == '__main__':

    """set the urls"""
    url_users = 'https://dummyapi.io/data/v1/user?page='
    url_posts = 'https://dummyapi.io/data/v1/post?page='
    url_comments = 'https://dummyapi.io/data/v1/comment?page='

    """get the users and posts (preview) from the server as json array"""
    fetched_users = fetch_data(url_base=url_users)
    fetched_posts = fetch_data(url_base=url_posts)

    """get the users and posts (full) from the server and then, set the objects in 
    an array. Furthermore, it checks dublication or a post/comment has an unknown owner."""
    users = user.get_full_users(fetched_users)
    posts = post.get_full_posts(fetched_posts, users)
    comments = comment.get_comments(url_comments, users, posts)

    """create the database if does not exist and then, open a connection and insert
    the values to the database. The function can handle the error from the database
    (dublication or other)"""
    mydb = connect_to_db()
    for u in users:
        insert_user_to_db(mydb, u)
    for p in posts:
        insert_post_to_db(mydb, p)
    for c in comments:
        insert_comment_to_db(mydb, c)
    close_db(mydb)