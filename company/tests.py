import datetime

from django.test import TestCase, Client

from position.models import (Experience,
                             Position)

from .models import (MainCategory,
                     SubCategory,
                     Company,
                     Salary,
                     CategoryToSalary)

class CompanyAppTest(TestCase):
    maxDiff = None

    def setUp(self):
        maincategory = MainCategory.objects.create(
            id = 1,
            name = 'Develop'
        )

        subcategory_one = SubCategory.objects.create(
            id            = 1,
            main_category = maincategory,
            name          = 'Python Developer',
            image         = 'http://python.com'
        )

        subcategory_two = SubCategory.objects.create(
            id            = 2,
            main_category = maincategory,
            name          = 'Frontend Developer',
            image         = 'http://front.com'
        )

        company = Company.objects.create(
            id       = 1,
            name     = 'Naver',
            field    = 'IT, Contents',
            logo_url = 'http://www.naver.com',
            is_premium = True,
            banner_url = 'http://naver.com/banner-url',
        )

        experience = Experience.objects.create(
            id   = 1,
            year = 1
        )

        position = Position.objects.create(
            id          = 1,
            category    = subcategory_one,
            company     = company,
            experience  = experience,
            like        = 100,
            title       = 'Machine Learning Engineer',
            expiry_date = datetime.date(2020, 10, 30),
        )

        salary = Salary.objects.create(
            id      = 1,
            year    = 1,
            payroll = 3000
        )

        salary_two = Salary.objects.create(
            id      = 2,
            year    = 2,
            payroll = 4000
        )

        CategoryToSalary.objects.create(
            category = subcategory_one,
            salary   = salary
        )

        CategoryToSalary.objects.create(
            category = subcategory_one,
            salary   = salary_two
        )

    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Company.objects.all().delete()
        Experience.objects.all().delete()
        Position.objects.all().delete()

    def test_category_list_view(self):
        c = Client()
        response = c.get('/companies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "category_list": [
                    {
                        "id": 1,
                        "name": "Python Developer",
                        "image": "http://python.com"
                    },
                    {
                        "id": 2,
                        "name": "Frontend Developer",
                        "image": "http://front.com"
                    }
                ]
            }
        )

    def test_company_slider_view(self):
        c = Client()
        response = c.get('/companies/slider')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "company_list": [
                    {
                    "company_name": "Naver",
                    "banner_url": "http://naver.com/banner-url",
                    "title": [
                        "Machine Learning Engineer"
                    ],
                    "title_id": 1
                    }
                ]
            }
        )

    def test_salary_view(self):
        c = Client()
        response = c.get('/companies/salary')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "salary_list": [
                    {
                        "main_category": "Develop",
                        "sub_category": "Python Developer",
                        "salary": [
                            [
                                1,
                                3000
                            ],
                            [
                                2,
                                4000
                            ]
                        ]
                    },
                    {
                        "main_category": "Develop",
                        "sub_category": "Frontend Developer",
                        "salary": []
                    }
                ]
            }
        )

    def test_average_salary_view(self):
        c = Client()
        response = c.get('/companies/average/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "category_average": {
                    "junior": None,
                    "first": 3000.0,
                    "second": 4000.0,
                    "third": None,
                    "fourth": None,
                    "fifth": None,
                    "sixth": None,
                    "seventh": None,
                    "eigth": None,
                    "ninth": None,
                    "tenth": None,
                }
            }
        )

    def test_average_salary_fail_view(self):
        c = Client()
        response = c.get('/companies/average/3')
        self.assertEqual(response.status_code, 404)
