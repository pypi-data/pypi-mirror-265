import regex as re
from django.db import connection


def fromDatabase(model, db_column, item):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {db_column} FROM {model} WHERE {db_column} = %s", [item])
        row = cursor.fetchone()
        print("*" * 100, row)
        return row


def unique(item, frags, req, messages):
    if req[item]:
        db_column = item
        model = frags[1]
        attribute = frags[0]
        record = fromDatabase(model, db_column, item)
        if record:
            print('record', record)
            name = f'{item}_unique'
            if 'unique' in messages.keys():
                return messages["unique"]
            else:
                return f'{item.title()} must be unique'


def max(item, frags, req, messages):
    if req[item]:
        max_value = frags[1]
        if len(req[item]) > int(max_value):
            name = f'{item}_max'
            if 'max' in messages.keys():
                return messages["max"]
            else:
                return f'{item.title()} must not be greater than {max_value} characters'


def min(item, frags, req, messages):
    if req[item]:
        min_value = frags[1]
        if len(req[item]) < int(min_value):
            name = f'{item}_max'
            if 'max' in messages.keys():
                return messages["max"]
            else:
                return f'{item.title()} must be alteast {min_value} characters'


def required(item, frags, req, messages):
    value = frags[0]
    if not req[item]:
        name = f'{item}.required'
        if name in messages.keys():
            return messages[name]
        else:
            return f'{item.title()} cannot be empty'


def email(item, frags, req, messages):
    if req[item]:
        em = req['email']
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, em):
            name = "email"
            if 'email' in messages.keys():
                return messages["email"]
            else:
                return f'Invalid email, please provide valid email id'


def numeric(item, frags, req, messages):
    if req[item]:
        if not str(req[item]).isnumeric():
            if 'numeric' in messages.keys():
                return messages["numeric"]
            else:
                return f'Not a number: {item.title()} should be a number'


def boolean(item, frags, req, messages):
    if req[item]:
        if type(req[item]) is not bool:
            if 'boolean' in messages.keys():
                return messages["boolean"]
            else:
                return f'Type error: {item.title()} should be either 1/0 or true false'


def string(item, frags, req, messages):
    if req[item]:
        if not isinstance(req[item], str):
            if 'string' in messages.keys():
                return messages["string"]
            else:
                return f'Type error: {item.title()} should be a string'


def uppercase(item, frags, req, messages):
    if req[item]:
        if not str(req[item]).isupper():
            if 'uppercase' in messages.keys():
                return messages["uppercase"]
            else:
                return f'Type error: {item.title()} should be uppercase'
