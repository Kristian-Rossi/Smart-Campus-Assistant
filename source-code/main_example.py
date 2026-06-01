class User:
    def __init__(self, user_name, email):
        self.user_name: str = user_name
        self.email: str = email

    def get_email(self, some_var):
        return self.email
    
    def another_example_function():
        return self.get_email



if __name__ == "__main__":
    user = User("kris.rossi", "kris@gmail.com")

    users = [
        User("kris.rossi", "kris@gmail.com"),
        User("nick.rossi", "nick@gmail.com")
    ]
    
    for user in users:
        print(user.user_name)
        print(user.email)
    