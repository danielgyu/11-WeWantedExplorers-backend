import datetime

from django.test import TestCase, Client

from .models import (Position,
                     Experience,
                     Description,
                     Image,
                     Address,
                     Tag,
                     Label)

from company.models import (MainCategory,
                            SubCategory,
                            Company,
                            CategoryToCompany)
class PositionViewTest(TestCase):
    maxDiff = None

    def setUp(self):
        maincategory = MainCategory.objects.create(
            id   = 1,
            name = 'Develop'
        )

        subcategory = SubCategory.objects.create(
            id            = 1,
            main_category = maincategory,
            name          = 'Python Developer',
            image         = 'http://www.daum.net',
        )

        subcategory_two = SubCategory.objects.create(
            id = 2,
            main_category = maincategory,
            name = 'Frontend Developer',
            image = 'http://frontend.com',
        )

        company = Company.objects.create(
            id       = 1,
            name     = 'Naver',
            field    = 'IT, Contents',
            logo_url = 'http://www.naver.com',
        )

        company_two = Company.objects.create(
            id       = 2,
            name     = 'Tesla',
            field    = 'Vehicle',
            logo_url = 'http://www.tesla.com'
        )

        experience = Experience.objects.create(
            id   = 1,
            year = 1
        )

        experience_two = Experience.objects.create(
            id   = 2,
            year = 2
        )

        position = Position.objects.create(
            id          = 1,
            category    = subcategory,
            company     = company,
            experience  = experience,
            like        = 100,
            title       = 'Machine Learning Engineer',
            expiry_date = datetime.date(2020, 10, 30),
        )

        position_two = Position.objects.create(
            id          = 2,
            category    = subcategory_two,
            company     = company_two,
            experience  = experience_two,
            like        = 50,
            title       = 'Computer Vision Engineer',
            expiry_date = datetime.date(2020,11,1),
        )

        description = Description.objects.create(
            id            = 1,
            position      = position,
            intro         = "Welcome to Naver",
            duty          = 'Machine Learning Development',
            qualification = 'Wecode graduate',
            preference    = 'Positive mentality',
            benefit       = 'Unlimited vacation leave'
        )

        Image.objects.bulk_create([
            Image(id = 1, position = position, url = 'http://www.google.com'),
            Image(id = 2, position = position, url = 'http://www.facebook.com'),
            Image(id = 3, position = position_two, url = 'http://tesla.com/1'),
            Image(id = 4, position = position_two, url = 'http://tesla.com/2'),
        ])

        Address.objects.create(
            id         = 1,
            position   = position,
            country    = 'Korea',
            city       = 'Seoul',
            line       = 'Seonlung Wework',
            latitude   = 37.5009452,
            longtitude = 127.0361278
        )

        Address.objects.create(
            id = 2,
            position = position_two,
            country = 'USA',
            city = 'California',
            line = 'Long Beach',
            latitude = 95.0000001,
            longtitude = 155.0000002,
        )

        tag1 = Tag.objects.create(
            id   = 1,
            name = 'Stock option'
        )

        tag2 = Tag.objects.create(
            id = 2,
            name = 'Free lunch'
        )

        Label.objects.create(
            id       = 1,
            position = position,
            tag      = tag1
        )

        Label.objects.create(
            id = 2,
            position = position,
            tag = tag2
        )

    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Company.objects.all().delete()
        CategoryToCompany.objects.all().delete()
        Position.objects.all().delete()
        Experience.objects.all().delete()
        Description.objects.all().delete()
        Image.objects.all().delete()
        Address.objects.all().delete()
        Tag.objects.all().delete()
        Label.objects.all().delete()

    def test_detail_view(self):
        c = Client()
        response = c.get('/positions/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "detail": {
                    "title": "Machine Learning Engineer",
                    "likes": 100,
                    "img": [
                        "http://www.google.com",
                        "http://www.facebook.com"
                    ],
                    "company": "Naver",
                    "country": "Korea",
                    "city": "Seoul",
                    "tags": [
                        "Stock option",
                        "Free lunch"
                    ],
                    "intro": "Welcome to Naver",
                    "duty": "Machine Learning Development",
                    "qualification": "Wecode graduate",
                    "preference": "Positive mentality",
                    "benefit": "Unlimited vacation leave",
                    "expiry_date": "2020-10-30",
                    "location": "Seonlung Wework",
                    "latitude": '37.5009452',
                    "longitude": '127.0361278',
                    "company_field": "IT, Contents"
                }
            }
        )

    def test_detail_view_fail(self):
        c = Client()
        response = c.get('/positions/10')
        self.assertEqual(response.status_code, 404)

    def test_logo_view(self):
        c = Client()
        response = c.get('/positions/logo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "logo_list": [
                    {
                        "logo": "http://www.naver.com"
                    },
                    {
                        "logo": "http://www.tesla.com"
                    }
                ]
            }
        )

    def test_position_view(self):
        c = Client()
        response = c.get('/positions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "position_list": [
                    {
                        "id": 1,
                        "title": "Machine Learning Engineer",
                        "likes": 100,
                        "company": "Naver",
                        "country": "Korea",
                        "city": "Seoul",
                        "img": "http://www.google.com"
                    },
                    {
                        "id": 2,
                        "title": "Computer Vision Engineer",
                        "likes": 50,
                        "company": "Tesla",
                        "country": "USA",
                        "city": "California",
                        "img": "http://tesla.com/1"
                    }
                ]
            }
        )

    def test_location_filter_view(self):
        c = Client()
        response = c.get('/positions', {'country': 'Korea', 'city' : 'Seoul', 'district' : 'Seonlung'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "position_list": [
                    {
                        "id": 1,
                        "title": "Machine Learning Engineer",
                        "likes": 100,
                        "company": "Naver",
                        "country": "Korea",
                        "city": "Seoul",
                        "img": "http://www.google.com"
                    }
                ]
            }
        )

    def test_experience_filter_view(self):
        c = Client()
        response = c.get('/positions', {'exp': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "position_list": [
                    {
                        "id": 2,
                        "title": "Computer Vision Engineer",
                        "likes": 50,
                        "company": "Tesla",
                        "country": "USA",
                        "city": "California",
                        "img": "http://tesla.com/1"
                    }
                ]
            }
        )

    def test_offset_filter_view(self):
        c = Client()
        response = c.get('/positions', {'offset': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "position_list": [
                    {
                        "id": 2,
                        "title": "Computer Vision Engineer",
                        "likes": 50,
                        "company": "Tesla",
                        "country": "USA",
                        "city": "California",
                        "img": "http://tesla.com/1"
                    }
                ]
            }
        )

    def test_offset_filter_empty_view(self):
        c = Client()
        response = c.get('/positions', {'offset': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "position_list": []
            }
        )

    def test_category_filter_view(self):
        c = Client()
        response = c.get('/positions', {'category': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "position_list": [
                    {
                        "id": 2,
                        "title": "Computer Vision Engineer",
                        "likes": 50,
                        "company": "Tesla",
                        "country": "USA",
                        "city": "California",
                        "img": "http://tesla.com/1"
                    }
                ]
            }
        )

    def test_category_filter_empty_view(self):
        c = Client()
        response = c.get('/positions', {'category': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "position_list": []
            }
        )
