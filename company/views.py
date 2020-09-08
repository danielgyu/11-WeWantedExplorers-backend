from random import sample

from django.db.models import Avg
from django.http      import JsonResponse
from django.views     import View

from position.models import (Tag,
                             Label)

from .models import (MainCategory,
                     SubCategory,
                     Company)

class SubcategoryView(View):
    def get(self, request):
        subcategory = SubCategory.objects.all()
        subcategory_list = [{
            'id'   : category.id,
            'name' : category.name,
            'image': category.image
        } for category in subcategory]

        return JsonResponse({'category_list' : subcategory_list}, status = 200)

class PremiumCompanyView(View):
    def get(self, request):
        companies = Company.objects.prefetch_related('position_set').filter(is_premium = True)

        company_list = [{
            'company_name' : company.name,
            'banner_url'   : company.banner_url,
            'title'        : [c.get('title') for c in company.position_set.values('title').distinct()],
            'title_id'     : company.position_set.first().id,
        } for company in companies]

        return JsonResponse({'company_list' : company_list}, status = 200)

class SalaryView(View):
    def get(self, request):
        sub_categories = SubCategory.objects.all().prefetch_related('salary_set')
        salary_list = [{
            'main_category' : category.main_category.name,
            'sub_category'  : category.name,
            'salary'        : [salary for salary in\
                               category.salary_set.values_list('year', 'payroll').order_by('year')]
        } for category in sub_categories]

        return JsonResponse({'salary_list' : salary_list}, status = 200)

class AverageSalaryView(View):
    def get(self, request, id):
        if MainCategory.objects.filter(id = id).exists():
            average = {
                'junior'  : MainCategory.salary_average(id, 0),
                'first'   : MainCategory.salary_average(id, 1),
                'second'  : MainCategory.salary_average(id, 2),
                'third'   : MainCategory.salary_average(id, 3),
                'fourth'  : MainCategory.salary_average(id, 4),
                'fifth'   : MainCategory.salary_average(id, 5),
                'sixth'   : MainCategory.salary_average(id, 6),
                'seventh' : MainCategory.salary_average(id, 7),
                'eigth'   : MainCategory.salary_average(id, 8),
                'ninth'   : MainCategory.salary_average(id, 9),
                'tenth'   : MainCategory.salary_average(id, 10),
            }

            return JsonResponse({'category_average': average}, status = 200)

        else:
            return JsonResponse({'ERROR': 'ID_DOESNT_EXIST'}, status = 404)

class TagRecommendView(View):
    def get(self, request):
        tags = sample(list(Tag.objects.all()), 5)
        tag_list = [{
            'tag_id': tag.id,
            'tag_name': tag.name
        } for tag in tags]
        return JsonResponse({'tags' : tag_list}, status = 200)

class CompanyTagView(View):
    def get(self, request, id):
        labels = Label.objects.filter(tag__id = id)
        label_list = [{
            'company_name' : label.position.company.name,
            'logo_url'     : label.position.company.logo_url,
            'tags'         : [tag.name for tag in label.position.tag_set.all()]
        } for label in labels]

        return JsonResponse({'comany_tag' : label_list}, status = 200)
