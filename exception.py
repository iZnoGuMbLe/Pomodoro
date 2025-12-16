class UserNotFound(Exception):
    detail = 'User is not found'

class UserIncorrectPassword(Exception):
    detail = 'Incorrect password'