import json
import bcrypt
import jwt
import unittest

from django.test   import TestCase, Client

from .models       import UserAccount, UserInformation
from .validator    import Validate_password
from wwe.settings  import SECRET_KEY, ALGORITHM
from unittest.mock import patch, MagicMock

class EmailCheckerTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_emailchecker_post_success(self):
        client = Client()

        mocked_emailchecker = {
            "email"       : "rose7@naver.com"
        }

        response = client.post(
            '/user/intro', 
            json.dumps(mocked_emailchecker), 
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
        {"message": "SignUp"})
    
    def test_emailchecker_invalid_email(self):
        client = Client()

        mocked_emailchecker = {
            "email"       : "rose7naver.com"
        }

        response = client.post(
            '/user/intro', 
            json.dumps(mocked_emailchecker), 
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json()["message"])   
    #traceback처리를 해서 너무 길어서 assertTrue로 진행

    def test_emailchecker_KEYERROR(self):
        client = Client()

        mocked_emailchecker = {
            "eml"       : "rose7naver.com"
        }

        response = client.post(
            '/user/intro', 
            json.dumps(mocked_emailchecker), 
            content_type='application/json')
        self.assertEqual(response.status_code, 401) 
        self.assertEqual(response.json(),
        {"message": "KEY ERROR"}) 
   

class SignUpTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_signup_post_success(self):
        client = Client()

        mocked_signup = {
            "email"       : "rose7@naver.com",
            "name"        : "김준",
            "phone_number": "01011112222",
            "password"    : "123456",
        }

        response = client.post(
            '/user/signup', 
            json.dumps(mocked_signup), 
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json(), 
        {"message":"SUCCESS"})

    def test_signup_post_too_short_password(self):
        client = Client()

        mocked_signup = {
            "email"       : "rose7@naver.com",
            "name"        : "김준",
            "phone_number": "01011112222",
            "password"    : "1234",
        }

        response = client.post(
            '/user/signup', 
            json.dumps(mocked_signup), 
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json()['message']) 
    
    def test_signup_post_KEYERROR(self):
        client = Client()

        mocked_signup = {
            "emil"        : "rose7@naver.com",
            "name"        : "김준",
            "phone_number": "01011112222",
            "password"    : "1256",
        }

        response = client.post(
            '/user/signup', 
            json.dumps(mocked_signup), 
            content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
        {"message": "KEY ERROR"}) 


class SignInTest(TestCase):
    def setUp(self):
        input_password = "123456"
        password_crypt  = bcrypt.hashpw(
            input_password.encode('utf-8'),
            bcrypt.gensalt()).decode('utf-8')
        
        user = UserAccount.objects.create(
            email         = "rose7@naver.com",
            platform_type = "Wanted"
        )

        UserInformation.objects.create(
            name         = "김준",
            phone_number = "01011112222",
            password     = password_crypt,
            user_account = user
        )

    def tearDown(self):
        UserAccount.objects.all().delete()
        UserInformation.objects.all().delete()

    def test_signin_post_success(self):
        client = Client()

        mocked_signin = {
            "email"    : "rose7@naver.com",
            "password" : "123456"
        }

        response = client.post(
        '/user/signin', 
        json.dumps(mocked_signin), 
        content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["message"])
        self.assertTrue(response.json()["token"])

    def test_signin_post_invalid_password(self):
        client = Client()

        mocked_signin = {
            "email"    : "rose7@naver.com",
            "password" : "123456789"
        }

        response = client.post(
        '/user/signin', 
        json.dumps(mocked_signin), 
        content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
        {"message":"PASSWORD_ERROR"})

    def test_signin_post_KEYERROR(self):
        client = Client()

        mocked_signin = {
            "email"    : "rose7@naver.com",
            "paw=ord"  : "123456789"
        }

        response = client.post(
        '/user/signin', 
        json.dumps(mocked_signin), 
        content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
        {"message": "KEY ERROR"}) 


class GoogleSignInTest(TestCase):
    def setUp(self):
        user = UserAccount.objects.create(
            email         = "rose7@google.com",
            platform_type = "Google"
        )

    def tearDown(self):
        UserAccount.objects.all().delete()
        UserInformation.objects.all().delete()

    @patch('user.views.requests')
    def test_google_signin_get_success(self, mocked_request):
        class FakeResponse:
            def json(self):
                return {
                    "email" : "rose7@google.com", 
                    "sub"   : "21313qweqeq", 
                    "azp"   : "100083625"
                }

        mocked_request.get = MagicMock(return_value = FakeResponse())
        client = Client()
        header = {'Authorization' : 'fake_goolge_token'}
        response = client.get(
            '/user/googlesignin', 
            content_type = 'application/json', 
            **header)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["message"])
        self.assertTrue(response.json()["access_token"])

    @patch('user.views.requests')
    def test_goolge_signin_get_not_exist_email_in_DB(self, mocked_request):
        class FakeResponse:
            def json(self):
                return {
                    "email" : "sunflower2@google.com", 
                    "sub"   : "21313qweqeq", 
                    "azp"   : "100083625"
                }

        mocked_request.get = MagicMock(return_value = FakeResponse())
        client = Client()
        header = {'Authorization' : 'fake_goolge_token'}
        response = client.get(
            '/user/googlesignin', 
            content_type = 'application/json', 
            **header)
            
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json(),
        {"message": "sunflower2@google.com"})

    def test_goolge_signin_post_for_signup_success(self):
        client = Client()

        mocked_signup = {
            "email"         : "sunflower2@google.com",
            "name"          : "김준",
            "phone_number"  : "01011112222",
        }

        response = client.post(
            '/user/googlesignin', 
            json.dumps(mocked_signup), 
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json(), 
        {"message": "SignUp completed"})

class ApplicationTest(TestCase):
    
