from django.core.cache import cache
from django.db.models  import Q, Avg
from django.http       import JsonResponse
from django.shortcuts  import render
from django.views      import View

from company.models import Company

from .models import Position

class PositionView(View):
    def get(self, request):
        d_category = request.GET.get('category', None)
        f_country  = request.GET.get('country', '')
        f_city     = request.GET.get('city', '')
        f_district = request.GET.get('district', '')
        f_exp      = request.GET.get('exp', None)
        f_sort     = request.GET.get('sort', None)
        offset     = int(request.GET.get('offset', 0))
        limit      = offset + 20
        positions = cache.get_or_set('positions',
                                     Position.objects.prefetch_related('category', 'image_set',
                                                                      'company', 'address',
                                                                      'experience').all())

        if d_category:
            positions = positions.filter(category__id = d_category)

        q = Q()
        # 필터링에 국가, 지역 또는 상셎역이 설정됐을 경우
        if f_country or f_city or f_district:
            q &= Q(address__country__contains = f_country)
            q &= Q(address__city__contains = f_city)
            q &= Q(address__line__contains = f_district)
            positions = positions.filter(q).distinct()

        # 필터링에 경력이 설정됐을 경우
        if f_exp:
            positions = positions.filter(experience__year = f_exp)

        # 인기순(like) 및 최신순(id) 정렬
        if f_sort:
            positions = positions.order_by(f'-{f_sort}')

        position_list = [{
            'id'      : position.id,
            'title'   : position.title,
            'likes'   : position.like,
            'company' : position.company.name,
            'country' : position.address.country,
            'city'    : position.address.city,
            'img'     : position.image_set.first().url,
        } for position in positions[offset:limit]]

        return JsonResponse({'position_list' : position_list}, status = 200)

class PositionDetailView(View):
    def get(self, request, id):
        if Position.objects.filter(id = id).exists():
            position = Position.objects.prefetch_related('description', 'image_set', 'address',
                                                         'tag_set', 'label_set', 'company').get(id = id)
            detail = {
                'title'         : position.title,
                'likes'         : position.like,
                'img'           : [img.url for img in position.image_set.all()],
                'company'       : position.company.name,
                'country'       : position.address.country,
                'city'          : position.address.city,
                'tags'          : [label.tag.name for label in position.label_set.all()],
                'intro'         : position.description.intro,
                'duty'          : position.description.duty,
                'qualification' : position.description.qualification,
                'preference'    : position.description.preference,
                'benefit'       : position.description.benefit,
                'expiry_date'   : position.expiry_date,
                'location'      : position.address.line,
                'latitude'      : position.address.latitude,
                'longitude'     : position.address.longtitude,
                'company_field' : position.company.field
            }

            return JsonResponse({'detail' : detail}, status = 200)

        else:
            return JsonResponse({'Error' : 'POSITION_DOES_NOT_EXIST'}, status = 404)

class LogoView(View):
    def get(self, request):
       companies = Company.objects.all().prefetch_related('position_set')
       companies = companies.annotate(likes=Avg('position__like'))
       logo_list = [{
           'logo' : company.logo_url,
       } for company in companies]

       return JsonResponse({'logo_list' : logo_list}, status = 200)
