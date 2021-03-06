
import requests
import json
from ConfigParser import SafeConfigParser
import time
import os
import sys


class Config:
    def __init__(self):
        """Creating object of SafeConfigParser() class to get access to it's methods and attributes"""
        self.parser = SafeConfigParser()
        """Checking if config file exists"""
        if os.path.isfile('config.ini'):
            self.parser.read('config.ini')
        else:
            print('No config.ini found under root folder.')
            # Shut down Python
            sys.exit()
        # Creating variables with values from config.ini
        self.admin_login = self.parser.get('Server', 'admin')
        self.password = self.parser.get('Server', 'password')
        self.test_path = self.parser.get('Server', 'testpath')
        self.puser = self.parser.get('Server', 'puser')


# Define class for sexy looking response object
class Response:
    def __init__(self):
        self.http_code = None
        self.body = dict()
        self.headers = dict()


# Define class to store all methods we need for framework
class Calls:
    def __init__(self):
        # Creating object of class Config()
        self.config = Config()
        # Creating variable with string to return it in case there is no json
        self.no_json = 'noJson'

    def create_folder(self, folder_name, domain=None, username=None, password=None,
                      content_type=None, accept=None, method=None, test_path=None):
        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'POST'
        if accept is None:
            accept = 'application/json'
        if content_type is None:
            content_type = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/fs'
        url = domain + endpoint + test_path + folder_name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        data = dict()
        data['action'] = 'add_folder'
        data = json.dumps(data)
        # Request method returning server response to r
        r = requests.request(
            url=url,
            auth=(username, password),
            headers=headers,
            data=data,
            method=method
        )

        # Fist: Trying to parse json and convert it to Pythonic dict.
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            # If parsing failed then check, maybe method was 'OPTIONS'
            if method == 'OPTIONS':
                json_resp = r.content
            # And finally return no_json string to json_resp variable
            else:
                json_resp = self.no_json
        # Putting processed r.content into r.json
        r.json = json_resp
        # Creating object of class Response()
        response = Response()
        response.http_code = r.status_code
        response.body = r.json
        response.headers = r.headers
        print('\n' + str(response.http_code))
        return response

    def delete_folder(self, folder_name, domain=None, username=None, password=None,
                      content_type=None, accept=None, method=None, test_path=None):
        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'DELETE'
        if accept is None:
            accept = 'application/json'
        if content_type is None:
            content_type = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/fs'
        url = domain + endpoint + test_path + folder_name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        r = requests.request(
            url=url,
            auth=(username, password),
            headers=headers,
            method=method
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            if method == 'OPTIONS':
                json_resp = r.content
            else:
                json_resp = self.no_json

        r.json = json_resp
        response = Response()
        response.http_code = r.status_code
        response.body = r.json
        response.headers = r.headers
        print('\n' + str(response.http_code))
        return response

    def set_perms(self, folder_name, permission, user, domain=None, username=None, password=None,
                  content_type=None, accept=None, method=None, test_path=None):
        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'POST'
        if accept is None:
            accept = 'application/json'
        if content_type is None:
            content_type = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/perms/folder'
        url = domain + endpoint + test_path + folder_name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        data = dict()
        data['permission'] = permission
        data['users'] = list()
        data['users'].append(user)
        data = json.dumps(data)
        # Request method returning server response to r
        r = requests.request(
            url=url,
            auth=(username, password),
            headers=headers,
            data=data,
            method=method
        )

        # Fist: Trying to parse json and convert it to Pythonic dict.
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            # If parsing failed then check, maybe method was 'OPTIONS'
            if method == 'OPTIONS':
                json_resp = r.content
            # And finally return no_json string to json_resp variable
            else:
                json_resp = self.no_json
        # Putting processed r.content into r.json
        r.json = json_resp
        # Creating object of class Response()
        response = Response()
        response.http_code = r.status_code
        response.body = r.json
        response.headers = r.headers
        print('\n' + str(response.http_code))
        return response

    # Defining static(nothing to do with parent class) method, which generates random
    @staticmethod
    def gen_random_name():
        return 'dynamic_name_%s' % str(time.time()).replace('.', '')

    def test_create_and_delete_100_folders_in_a_row(self):
        folder_name = self.calls.gen_random_name()
        for i in range(100):
            resp = self.calls.create_folder(folder_name + str(i))
            assert resp.http_code == httplib.CREATED
            assert resp.body == self.calls.no_json
        for i in range(100):
            resp = self.calls.delete_folder(folder_name + str(i))
            assert resp.http_code == httplib.OK
            assert resp.body == self.calls.no_json

    def test_perms(self):
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Full')
        assert resp.http_code == httplib.OK
        resp = self.calls.create_folder(folder_name, username=self.config.puser, test_path='%s/%s' %
                                                                                           (self.config.test_path, folder_name))
        assert resp.http_code == httplib.CREATED