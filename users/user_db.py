from sortedcontainers import SortedSet

class User:
    """
    preferences is list[bool] - size 3
    [email, phone, whatspp] true for yes and false for no
    """

    def __init__(self, id, firstname, lastname, email, phone, preferences):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.preferences = preferences
        self.followers = SortedSet()

    def print_user(self):
        print(f"Name: {self.firstname} {self.lastname}")

    def print_user_info(self):
        print(f"Name: {self.firstname} {self.lastname} \nEmail: {self.email} \nPhone: {self.phone}")


class UserDB:
    def __init__(self):
        self.__userDict = {}
        self.__id_set = SortedSet([i for i in range(100000)])

    def get_all_users(self):
        for user in self.__userDict:
            user.print_user()

    def get_all_users_info(self):
        for user in self.__userDict:
            user.print_user_info()
            print("\n")

    def add_user(self, user):
        self.__userDict[user.id] = user

    def delete_user(self, id):
        if id in self.__userDict:
            del self.__userDict[id]
    
    def get_preferences_by_id(self, id):
        user = self.__userDict.get(id, None)
        if user:
            return user.preferences
        return [False] * 3

    def get_followers(self, id):
        user = self.__userDict.get(id, None)

    def follow_user(self, from_id, to_id):
        user = self.__userDict.get(from_id, None)
        if user:
            user.followers.add(to_id)

    def unfollow_user(self, from_id, to_id):
        user = self.__userDict.get(from_id, None)
        if user:
            user.followers.remove(to_id)
