import requests
from user import User as user
from post import Post as post
from comment import Comment as comment

def fetch_data(url_base):
    headers = {'app-id': '6240aa8892ac1b1186be8d15'}
    page = 0
    # correct me
    limit = 5
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

        return json_list


if __name__ == '__main__':
    url_users = 'https://dummyapi.io/data/v1/user?page='
    url_posts = 'https://dummyapi.io/data/v1/post?page='
    url_comments = 'https://dummyapi.io/data/v1/comment?page='

    fetched_users = fetch_data(url_base=url_users)
    # fetched_posts = fetch_data(url_base=url_posts)

    users = user.get_full_users(fetched_users)
    # posts = post.get_full_posts(fetched_posts, users)
    # comments = comment.get_comments(url_comments, users, posts)

    # print(users, posts, comments)