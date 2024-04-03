class User:
    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.password = password

    def save(self, users_collection):
        users_collection.insert_one(
            {
                "username": self.username,
                "name": self.name,
                "email": self.email,
                "password": self.password,
            }
        )

    @staticmethod
    def find_by_username(users_collection, username):
        return users_collection.find_one({"username": username})

    @staticmethod
    def find_by_email(users_collection, email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def update_password(users_collection, username, password):
        users_collection.update_one({"username": username}, {"$set": {"password": password}})
