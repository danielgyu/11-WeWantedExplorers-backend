from django.http import JsonResponse
from django.views import View

from company.models import SubCategory

class SubcategoryView(View):
    def get(self, request):
        subcategory = SubCategory.objects.all()
        subcategory_list = [{
            'name' : category.name,
            'image': category.image
        } for category in subcategory]

        return JsonResponse({'category_list' : subcategory_list}, status = 200)
