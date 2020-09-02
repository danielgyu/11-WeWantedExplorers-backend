import json
import unittest
import traceback

from django.test import TestCase, Client

from .models     import (
    Resume,
    Career,
    Accomplishment,
    Education,
    AwardHistory,
    ForeignLanguage,
    LanguageTest,
    Link,
)
from user.models import UserAccount, UserInformation

class NewResumeTest(TestCase):
    def setUp(self):
        ua = UserAccount.objects.create(
            email         = "rose7@naver.com",
            platform_type = "Wanted",
        )
        UserInformation.objects.create(
            name         = "김준",
            phone_number = "01030004000",
            password     = "123456",
            user_account = ua
        )

    def tearDown(self):
        UserAccount.objects.all().delete()
        UserInformation.objects.all().delete()

    def test_new_resume_post_not_success(self):
        client = Client()
  
        mocked_newresume = {
            "user_email"     : "rose7@naver.com",
            "title"          : "이력서1",
            "writer_name"    : "김준",
            "email"          : "rose7@naver.com",
            "phone_number"   : "01030004000",
            "description"    : "신실하고 성실한 사람입니다. 항상 열심히하겠습니다"*100,
            "career"         : [],
            "education"      : [],
            "awardhistory"   : [],
            "foreignlanguage": [],
            "link"           : []
        }

        response = client.post(
            '/cv/new', 
            json.dumps(mocked_newresume), 
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {"message": "SUCCESS"})

    def test_new_resume_post_not_enough_postlength(self):
        client = Client()
  
        mocked_newresume = {
            "user_email"     : "rose7@naver.com",
            "title"          : "이력서1",
            "writer_name"    : "김준",
            "email"          : "rose7@naver.com",
            "phone_number"   : "01030004000",
            "description"    : "신실하고 성실한 사람입니다. 항상 열심히하겠습니다",
            "career"         : [],
            "education"      : [],
            "awardhistory"   : [],
            "foreignlanguage": [],
            "link"           : []
        }

        response = client.post(
            '/cv/new', 
            json.dumps(mocked_newresume), 
            content_type='application/json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json(),
        {"message": "현재 글자수 59자"})   

    def test_new_resume_post_blank_title(self):
        client = Client()
  
        mocked_newresume = {
            "user_email"     : "rose7@naver.com",
            "title"          : "이력서",
            "writer_name"    : "김준",
            "email"          : "rose7@naver.com",
            "phone_number"   : "01030004000",
            "description"    : "신실하고 성실한 사람입니다. 항상 열심히하겠습니다",
            "career"         : [],
            "education"      : [],
            "awardhistory"   : [],
            "foreignlanguage": [],
            "link"           : []
        }

        response = client.post(
            '/cv/new', 
            json.dumps(mocked_newresume), 
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json()['message'])
            
class MainResumeTest(TestCase):
    def setUp(self):
        ua = UserAccount.objects.create(
            email         = "1@2.com",
            platform_type = "Wanted",
        )
        user = UserInformation.objects.create(
            name         = "김준",
            phone_number = "01030004000",
            password     = "123456",
            user_account = ua
        )
        Resume.objects.create(
            title            = "이력서1",
            writer_name      = "김준",
            email            = "rose7@naver.com",
            phone_number     = "01030004000",
            description      = "신실하고 성실한 사람입니다. 항상 열심히하겠습니다",
            completion_status= "작성 중",
            is_fileupload    = False,
            fileurl          = None,
            user_information = user
        )

    def tearDown(self):
        UserAccount.objects.all().delete()
        UserInformation.objects.all().delete()
        Resume.objects.all().delete()

    def test_mainresume_get_success(self):
        client = Client()
        header   = {
            "Authorization" : "accesstoken"
        }
        response = client.get(
            '/cv/list',
            content_type = 'application/json',
             **header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {"resume":[{
            "id"                : 1,
            "title"             : "이력서1",
            "created_at"        : "2020-09-08",
            "completion_status" : "작성 중",
        }]})
        