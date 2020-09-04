from django.test import TestCase, Client

from .models import MainCategory, SubCategory

class SubcategoryViewTest(TestCase):

    def setUp(self):
        maincategory = MainCategory.objects.create(
            id = 1,
            name = 'Develop'
        )

        SubCategory.objects.create(
            id            = 1,
            main_category = maincategory,
            name          = 'Python Developer',
            image         = 'http://python.com'
        )

        SubCategory.objects.create(
            id            = 2,
            main_category = maincategory,
            name          = 'Frontend Developer',
            image         = 'http://front.com'
        )

    def test_category_list_view(self):
        c = Client()
        response = c.get('/companies')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(

            response.json(),
            {
                "category_list": [
                    {
                        "name": "Python Developer",
                        "image": "http://python.com"
                    },
                    {
                        "name": "Frontend Developer",
                        "image": "http://front.com"
                    }
                ]
            }
        )
