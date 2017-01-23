#!/usr/bin/env python3
# coding: utf-8

from bottle import error, route, response, request, run, default_app
from enum import Enum
from json import dumps
import datetime
import hashlib
import os
import subprocess

__basedir__ = os.path.abspath(os.path.dirname(__file__))

class Auth(Enum):
    success = 0
    invalid = 1
    missing = 2



def irsend(code_name):
    return subprocess.call(['irsend', 'SEND_ONCE', 'aircon', code_name])



def result_json(mode, value, result_code):
    success = bool(1 - result_code)
    message = ''

    if success :
        message = 'OK. ' + mode + ' -> ' + str(value) + '.' 
    else:
        message = 'NG. ' + mode + ' -> ' + str(value) + ' is not implemented.' 

    response.content_type = 'application:json'
    return dumps({'result': success, 'message': message, 'mode': mode, 'value': value })


    
def hash_passwd_list():
    with open(__basedir__ + '/hash_passwd', 'r') as passwd_file:
    	passwd = passwd_file.readlines()
    passwd_list = [x.split(':') for x in passwd]
    return passwd_list, passwd



def generate_token(password):
    # おもちゃなのでいつか直す
    today = datetime.date.today()
    token = password
    for i in range(0, today.year + today.month):
        token = hashlib.sha512(token.encode('ascii')).hexdigest()
    return token;



def check_account(username, password):
    passwd_list, passwd = hash_passwd_list()
    user_info = [x for x in passwd_list if x[0] == username]
    try:
        if password == user_info[0][1]:
            return Auth.success, user_info
        else:
            return Auth.invalid, None
    except:
        return Auth.missing, None



def check_auth():
    try:
        username = request.params.username
        token = request.params.token

        print(username)
        print(token)

        passwd_list, passwd = hash_passwd_list()
        user_info = [x for x in passwd_list if x[0] == username]
        user_token = generate_token(user_info[0][1])
    except:
        return False

    return token == user_token



def need_login():
    response.content_type = 'application:json'
    return dumps({'result': False, 'message': 'NG. please login.' })



def write_state(state):
    with open(__basedir__ + '/state', 'w') as state_file:
        state_file.write(state)


### クソコード選手権
@route('/cool/<value:int>')
def cool(value):
    if not check_auth():
        return need_login()
    code_name = 'cool_' + str(value)
    result_code = irsend(code_name)
    if not result_code:
        write_state('cool:' + str(value))
    return result_json('cool', value, result_code)



@route('/dry/<value:int>')
def dry(value):
    if not check_auth():
        return need_login()
    code_name = 'warm_' + str(value)
    result_code = irsend(code_name)
    if not result_code:
        write_state('dry:' + str(value))
    return result_json('dry', value, result_code)



@route('/warm/<value:int>')
def warm(value):
    if not check_auth():
        return need_login()
    code_name = 'warm_' + str(value)
    result_code = irsend(code_name)
    if not result_code:
        write_state('warm:' + str(value))
    return result_json('warm', value, result_code)



@route('/off')
def off():
    if not check_auth():
        return need_login()
    code_name = 'off'
    result_code = irsend(code_name)
    if not result_code:
        write_state('power:off')
    return result_json('power', 'off', result_code)



@route('/check')
def off():
    if not check_auth():
        return need_login()

    response.content_type = 'application:json'
    return dumps({'result': True, 'message': 'OK. your accont is still alive.'})


@route('/login', method = 'POST')
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    response.content_type = 'application:json'

    status, user_info = check_account(username, password)
    if status == Auth.success:
        token = generate_token(user_info[0][1])
        return dumps({'result': True, 'message': 'OK. generated your access token.', 'token': token })
    elif status == Auth.invalid:
        return dumps({'result': False, 'message': 'NG. your password is wrong.' })
    else:
        return dumps({'result': False, 'message': 'NG. your account is missing.' })



@route('/state')
def state():
    response.content_type = 'application:json'

    try:
        with open(__basedir__ + '/state', 'r') as state_file:
            states = state_file.read().split(':')
        return dumps({'result': True, 'message': 'OK. current state [ ' + states[0] + ' : ' + states[1] + ' ].', 'raw_state': states, 'mode': states[0], 'value': states[1] })
    except:
        return dumps({'result': False, 'message': 'NG. state lost.'})



@error(404)
def on_error_404(error):
    response.content_type = 'application:json'
    return dumps({'result': False, 'message': 'NG. requested resource is not found.' })


    
@error(405)
def on_error_405(error):
    response.content_type = 'application:json'
    return dumps({'result': False, 'message': 'NG. nethod not allowd.' })
    


app = default_app()

if __name__ == '__main__':
    run(host='localhost', port=8001, debug=False, reloader=False, server='gunicorn', workers=5)
