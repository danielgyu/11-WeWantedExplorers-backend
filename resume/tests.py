import json
import unittest
import traceback
import jwt

from django.test  import TestCase, Client

from .models      import (
    Resume,
    Career,
    Accomplishment,
    Education,
    AwardHistory,
    ForeignLanguage,
    LanguageTest,
    Link,
)
from user.models  import UserAccount, UserInformation
from wwe.settings import SECRET_KEY, ALGORITHM

class NewResumeTest(TestCase):
    def setUp(self):
        ua = UserAccount.objects.create(
            email         = "rose8@naver.com",
            platform_type = "Wanted",
        )
        user = UserInformation.objects.create(
            name         = "김준",
            phone_number = "01030004000",
            password     = "123456",
            user_account = ua
        )
        self.token = jwt.encode({'user_id': user.id}, 
                        SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        UserAccount.objects.all().delete()
        UserInformation.objects.all().delete()
        Resume.objects.all().delete()
    
    def test_new_resume_post_success(self):
        client = Client()
        
        mocked_newresume = {
            "user_email" : "rose8@naver.com"
        }

        header = {"HTTP_Authorization" : self.token}
        response = client.post(
            '/cv/new', 

            json.dumps(mocked_newresume),
            **header,
            content_type='application/json',
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {"resume": 1 })
    
    def test_new_resume_post_invalid_email(self):
        client = Client()

        mocked_newresume = {
            "user_email" : "iris@nav.com"
        }

        header = {"HTTP_Authorization" : self.token}
        response = client.post(
            '/cv/new', 
            json.dumps(mocked_newresume), 
            **header,
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
        {'message': 'INVALID_EMAIL'})
    
    def test_new_resume_post_KEYERROR(self):
        client = Client()

        mocked_newresume = {
            "u_email" : "rose8@naver.com"
        }

        header = {"HTTP_Authorization" : self.token}
        response = client.post(
            '/cv/new', 
            json.dumps(mocked_newresume), 
            **header,
            content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
        {'message':'KEY ERROR'})
      
class ResumesTest(TestCase):
    def setUp(self):
        ua = UserAccount.objects.create(
            email         = "rose7@naver.com",
            platform_type = "Wanted",
        )
        user = UserInformation.objects.create(
            name         = "김준",
            phone_number = "01030004000",
            password     = "123456",
            user_account = ua
        )
        Resume.objects.create(
            title            = "김준",
            writer_name      = "김준",
            email            = "rose7@naver.com",
            phone_number     = "01030004000",
            description      = "안녕하세요 김준입니다",
            completion_status= "작성 중",
            is_fileupload    = False,
            fileurl          = None,
            user_information = user
        )
        self.token = jwt.encode({'user_id': user.id}, 
                        SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        UserAccount.objects.all().delete()
        UserInformation.objects.all().delete()
        Resume.objects.all().delete()

    def test_resumes_get_success(self):
        client = Client()
        
        header = {"HTTP_Authorization" : self.token}
        
        response = client.get(
            '/cv/list',
            **header,
            content_type = 'application/json',
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {"resume":[{
            "id"                : 3,
            "title"             : "김준",
            "created_at"        : "2020-09-10",
            "completion_status" : "작성 중",
        }]})

class ResumeDeleteView(TestCase):
    def setUp(self):
        ua = UserAccount.objects.create(
            email         = "rose7@naver.com",
            platform_type = "Wanted",
        )
        user = UserInformation.objects.create(
            name         = "김준",
            phone_number = "01030004000",
            password     = "123456",
            user_account = ua
        )
        Resume.objects.create(
            title            = "김준",
            writer_name      = "김준",
            email            = "rose7@naver.com",
            phone_number     = "01030004000",
            description      = "안녕하세요 김준입니다",
            completion_status= "작성 중",
            is_fileupload    = False,
            fileurl          = None,
            user_information = user
        )
        self.token = jwt.encode({'user_id': user.id}, 
                        SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        UserAccount.objects.all().delete()
        UserInformation.objects.all().delete()
        Resume.objects.all().delete()

    def test_delete_post_success(self):
        client = Client()

        header = {"HTTP_Authorization" : self.token}
        
        response = client.post(
            '/cv/delete/1', 
            **header,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {'message':'SUCCESS'})


# class ResumeTest(TestCase):
#     def setUp(self):
#         ua = UserAccount.objects.create(
#             email         = "rose7@naver.com",
#             platform_type = "Wanted",
#         )
#         user = UserInformation.objects.create(
#             name         = "김준",
#             phone_number = "01030004000",
#             password     = "123456",
#             user_account = ua
#         )
#         Resume.objects.create(
#             title            = "김준",
#             writer_name      = "김준",
#             email            = "rose7@naver.com",
#             phone_number     = "01030004000",
#             description      = "안녕하세요 김준입니다",
#             completion_status= "작성 중",
#             is_fileupload    = False,
#             fileurl          = None,
#             user_information = user
#         )

#     def tearDown(self):
#         UserAccount.objects.all().delete()
#         UserInformation.objects.all().delete()
#         Resume.objects.all().delete()

#     def test_resume_get_success(self):
#         client = Client()

#         header = {
#             "Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.M4rMmGTT6HWBuR5kI2EZi48qHbIuR0fMk4DaeOMJ-C4"}
#         response = client.get(
#             '/cv/1',  
#             content_type='application/json',
#              **header)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(),
#        {
#             "user_email"     : "rose7@naver.com",
#             "title"          : "김준",
#             "writer_name"    : "김준",
#             "email"          : "rose7@naver.com",
#             "phone_number"   : "01030004000",
#             "description"    : "안녕하세요 김준입니다",
#             "career"         : [],
#             "education"      : [],
#             "awardhistory"   : [],
#             "foreignlanguage": [],
#             "link"           : []
#         })

#     def test_new_resume_post_not_enough_postlength(self):
#         client = Client()
  
#         mocked_newresume = {
#             "user_email"     : "rose7@naver.com",
#             "title"          : "이력서1",
#             "writer_name"    : "김준",
#             "email"          : "rose7@naver.com",
#             "phone_number"   : "01030004000",
#             "description"    : "신실하고 성실한 사람입니다. 항상 열심히하겠습니다",
#             "career"         : [{
#                 "company_name" : "samsung",
#                 "department"   : "HR",
#                 "position"     : "freshman"
#             }],
#             "education"      : [{
#                 "school_name" : "Sejong University"
#             }],
#             "awardhistory"   : [],
#             "foreignlanguage": [{
#                 "name" : "English",
#                 "level": "InterMediate"
#             }],
#             "link"           : []
#         }

#         response = client.post(
#             '/cv/1', 
#             content_type='application/json')
#         self.assertEqual(response.status_code, 202)
#         self.assertEqual(response.json(),
#         {"message": "현재 글자수 59자"})   

#     def test_new_resume_post_blank_title(self):
#         client = Client()
  
#         mocked_newresume = {
#             "user_email"     : "rose7@naver.com",
#             "title"          : "이력서1",
#             "writer_name"    : "김준",
#             "email"          : "rose7@naver.com",
#             "phone_number"   : "01030004000",
#             "description"    : "신실하고 성실한 사람입니다. 항상 열심히하겠습니다",
#             "career"         : [{
#                 "company_name" : "samsung",
#                 "department"   : "HR",
#                 "position"     : "freshman"
#             }],
#             "education"      : [{
#                 "school_name" : "Sejong University"
#             }],
#             "awardhistory"   : [],
#             "foreignlanguage": [{
#                 "name" : "English",
#                 "level": "InterMediate"
#             }],
#             "link"           : []
#             }

#         response = client.post(
#             '/cv/1', 
#             json.dumps(mocked_newresume), 
#             content_type='application/json')
#         self.assertEqual(response.status_code, 401)
#         self.assertEqual(response.json(), {'message': "up"})