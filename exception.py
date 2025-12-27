class UserNotFound(Exception):
    detail = 'User is not found'

class UserIncorrectPassword(Exception):
    detail = 'Incorrect password'

class TokenExpired(Exception):
    detail = ' Token has expired'


class TokenNotCorrect(Exception):
    detail = "Token is incorrect"

class TaskNotFound(Exception):
    detail = "Task not found"