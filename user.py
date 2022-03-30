import requests
import re
from datetime import date
from dateutil import parser
import validators

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

    def validate(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.dateOfBirth = parser.parse(self.dateOfBirth).date()
        if not self.title in ["mr", "ms", "mrs", "miss", "dr", ""]:
            print('User - ', self.id, ', does not have validated title')
            return False
        elif len(self.firstName) < 2 and len(self.firstName) > 50:
            print('User - ', self.id, ', does not have validated firstName')
            return False
        elif len(self.lastName) < 2 and len(self.lastName) > 50:
            print('User - ', self.id, ', does not have validated lastName')
            return False
        elif not self.gender in ["male", "female", "other", ""]:
            print('User - ', self.id, ', does not have validated gender')
            return False
        elif not re.fullmatch(regex, self.email):
            print('User - ', self.id, ', does not have validated email')
            return False
        elif self.dateOfBirth < date(1900, 1, 1):
            print('User - ', self.id, ', does not have validated dateBirth')
            print(self.dateOfBirth)
            return False
        else:
            return True
        
    def is_dublicate(self, users_list):
        for user in users_list:
            if user.id == self.id:
                print('There is the same object')
                return True
        return False


    def get_full_users(usrs):
        headers = {'app-id': '6240aa8892ac1b1186be8d15'}
        users = []
        for user in usrs:
            url = 'https://dummyapi.io/data/v1/user/' + user['id']
            r = requests.get(url, headers=headers)
            user = User(r.json())
            if user.validate() and not user.is_dublicate(users):
                users.append(user)
        return users
