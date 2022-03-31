from wsgiref.validate import validator
import requests
import re
from datetime import date
from dateutil import parser
import validators

class User:
    def __init__(self, json):
        self.id = str(json['id'])
        self.title = str(json['title'])
        self.firstName = str(json['firstName'])
        self.lastName = str(json['lastName'])
        self.picture = str(json['picture'])
        self.gender = str(json['gender'])
        self.email = str(json['email'])
        self.dateOfBirth = str(json['dateOfBirth'])
        self.phone = str(json['phone'])
        self.location = json['location']
        self.registerDate = json['registerDate']
        self.updatedDate = json['updatedDate']

    def validate(self):
        self.dateOfBirth = parser.parse(self.dateOfBirth).date()
        if not self.title in ["mr", "ms", "mrs", "miss", "dr", ""]:
            print('User - ', self.id, ', does not have validated title')
            return False
        elif not validators.length(self.firstName, min=2, max=50):
            print('User - ', self.id, ', does not have validated firstName')
            return False
        elif not validators.length(self.lastName, min=2, max=50):
            print('User - ', self.id, ', does not have validated lastName')
            return False
        elif not self.gender in ["male", "female", "other", ""]:
            print('User - ', self.id, ', does not have validated gender')
            return False
        elif not validators.email(self.email):
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
