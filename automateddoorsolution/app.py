from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from flask import abort
import logging
import json
import random
import json

# from security import authenticate, identity

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
logging.basicConfig(level=logging.DEBUG)


def write_to_file(info, file, flag):
    if flag[0] == True:
        with open(file, 'a') as file:
            file.write(json.dumps(info))
            file.write('\n')
            app.logger.info(f"Sucessfully written to file {file}")
    else:
        app.logger.info("Could not write data to logs.txt")


"""Read data from data.json
"""
doors = []
heartbeat = []
employees = []

f = open('data.json', )
data = json.load(f)

for i in data['doors']:
    doors.append(i)
for i in data['heartbeat']:
    heartbeat.append(i)
for i in data['employees']:
    employees.append(i)
app.logger.info(heartbeat)
app.logger.info(doors)
f.close()

authentication_flag = False


class Authenticate(Resource):
    def get(self, type, door):
        if type == 'enter' or type == 'exit':
            for name in doors:
                if str(door) == str(name):
                    global authentication_flag
                    authentication_flag = True
                    app.logger.info(authentication_flag)
                    return f'{door} is a valid door, you can {type}'
            return f'{door} is not a valid door, you cannot {type}'
        else:
            abort(403, "Not a valid request")


api.add_resource(Authenticate, '/automate/action/<string:type>/door/<string:door>')


class Heartbeat(Resource):
    def get(self):
        heartbeats = random.choice(heartbeat)
        d = random.choice(doors)
        app.logger.info(heartbeats)
        if heartbeats == 'non-operational':
            abort(500, f"{d} is {heartbeats} ")
        else:
            return 200


api.add_resource(Heartbeat, '/automate/heartbeat')


class Validate(Resource):
    def post(self, type, door):
        global authentication_flag
        app.logger.info(authentication_flag)
        if authentication_flag:
            authentication_flag = False
            app.logger.info(authentication_flag)
            data = request.get_json()
            access_info = {'type':type, 'door': door, 'empId': data['empId']}
            if data['empId'] > 0:
                r = random.choices([True, False], [0.9, 0.1], k=1)
                app.logger.info("Random Choice To Write To File")
                app.logger.info(r)
                write_to_file(access_info, 'sucess_logs.txt', r)
                return {'Action': 'Success', 'access_info': access_info}
            else:
                return {'Action': 'Failed', 'Message': 'Invalid Employee ID'}
        else:
            return abort(401, "Authentication failed")


api.add_resource(Validate, '/automate/action/<string:type>/door/<string:door>')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
