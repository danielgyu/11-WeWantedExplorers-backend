import json
import bcrypt
import jwt
import traceback
import requests

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from wwe.settings           import ALGORITHM, SECRET_KEY
from .models                import (
    Resume, 
    Career, 
    Education, 
    AwardHistory, 
    ForeignLanguage,
    LanguageTest, 
    Link
    )
from .functions             import (
    Validate_title, 
    Validate_writername, 
    Validate_email,
    Validate_phone_number, 
    length_counter
    )
from user.models            import UserAccount
from user.decorator         import signin_decorator

class NewResumeView(View): # 새 이력서
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            if UserAccount.objects.filter(email=data['user_email']).exists():
                user = UserAccount.objects.get(
                    email=data['user_email']).userinfo.first()
                
                count = user.resume.filter(writer_name=user.name).count()

                resume = Resume(
                    title             = f"{user.name} {count}",
                    writer_name       = user.name,
                    email             = data['user_email'],
                    phone_number      = user.phone_number,
                    description       = f"안녕하세요 {user.name}입니다",
                    completion_status = '작성 중',
                    is_fileupload     = False,
                    fileurl           = None,
                    user_information  = user,
                )
                resume.full_clean()
                resume.save()
                return JsonResponse({'resume': resume.id }, status = 200)
            return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status = 401) 

class ResumesView(View): # 이력서 리스트
    @signin_decorator
    def get(self, request):
        user_id = request.user.userinfo.first().id
        resume_packs = Resume.objects.filter(user_information_id=user_id)
        body = {"resume":[{
            "id"                : resume.id,
            "title"             : resume.title,
            "created_at"        : resume.created_at,
            "completion_status" : resume.completion_status,
        } for resume in resume_packs]}
        return JsonResponse(body, status=200)

class ResumeDeleteView(View): #이력서 삭제
    @signin_decorator
    def delete(self, request, resume_id):
        try:
            Resume.objects.get(id = resume_id).delete()
            return JsonResponse({'message':'SUCCESS'}, status = 200)

        except Exception as exceptions: 
            return JsonResponse({'message':exceptions}, status = 400)

class ResumeView(View): # 기존 이력서 작성 페이지
    @signin_decorator
    def get(self, request, id):
        user_id = request.user.userinfo.first().id
        if Resume.objects.get(id=id).user_information != user_id:
            return JsonResponse({"message" : "FORBIDDEN"}, status=403)
        if Resume.objects.filter(id=id).exists() :
            resume = Resume.objects.prefetch_related(
            'career', 'education', 'award_history', 
            'foreign_language', 'link').get(id=id) 
            
            body = {
            "resume_id"      : id,
            "title"          : resume.title,
            "writer_name"    : resume.writer_name,
            "email"          : resume.email,
            "phone_number"   : resume.phone_number,
            "description"    : resume.description,
            "career"         : [{
                "company_name" : datum.company_name,
                "department"   : datum.department,
                "position"     : datum.position,
                "start_date"   : datum.start_date,
                "end_date"     : datum.end_date,
                "is_incumbent" : datum.is_incumbent,
            }for datum in resume.career.all()],

            "education"      : [{
                "school_name"      : datum.school_name,
                "major"            : datum.major,
                "degree"           : datum.degree,
                "research_content" : datum.research_content,
                "start_date"       : datum.start_date,
                "end_date"         : datum.end_date, 
                "is_attending"     : datum.is_attending
            }for datum in resume.education.all()],

            "award_history"   : [{
                "award_name" : datum.award_name,
                "detail"     : datum.detail,
                "date"       : datum.date
            }for datum in resume.award_history.all()],

            "foreignlanguage": [{
                "name"  : datum.name,
                "level" : datum.level,
            }for datum in resume.foreign_language.all()],

            "link" : [{
                "url"   : datum.url
            }for datum in resume.link.all()]
        }
            return JsonResponse(body, status=200)
        return JsonResponse({"message" : "INVALID ACCESS"}, status=400)
    
    @signin_decorator
    def post(self, request, id): #게시물 업데이트  
        data = json.loads(request.body)
        if Resume.objects.get(id=id).user_information != user_id:
            return JsonResponse({"message" : "FORBIDDEN"}, status=403)
        if Resume.objects.filter(id=id).exists() :
            try :
                resume = Resume.objects.prefetch_related(
                    'career', 'education', 'award_history', 
                    'foreign_language', 'link').filter(id=id)

                resume.update(
                        title        = data['title'],
                        writer_name  = data['writer_name'],
                        email        = data['email'],
                        phone_number = data['phone_number'],
                        description  = data['description']
                    )
                resume = resume.first()
                if data['career'] :
                    for datum in data['career']:
                        Career(
                            company_name = datum['company_name'], 
                            department   = datum['department'], 
                            position     = datum['position'], 
                            start_date   = datum['start_date'], 
                            end_date     = datum['end_date'], 
                            is_incumbent = datum['is_incumbent'],
                            resume       = resume
                        ).save()
                
                if data['education'] :
                    for datum in data["education"] :
                        Education(
                            school_name      = datum['school_name'],
                            major            = datum['major'],
                            degree           = datum['degree'],
                            research_content = datum['research_content'],
                            start_date       = datum['start_date'],
                            end_date         = datum['end_date'],
                            is_attending     = datum['is_atteding'],
                            resume           = resume
                        ).save() 

                if data['award_history'] :
                    for datum in data["award_history"] :
                        AwardHistory(
                            award_name = datum['award_name'],
                            detail     = datum['detail'],
                            date       = datum['date'],
                            resume     = resume
                        ).save()

                if data["foreignlanguage"] :
                    for datum in data["foreignlanguage"] :
                        ForeignLanguage(
                            name   = datum['name'],
                            level  = datum['level'],
                            resume = resume
                        ).save() 

                if data["link"] :
                    for datum in data["link"] :
                        Link(
                            url    = datum['url'],
                            resume = resume
                        ).save()
                
                total_length = length_counter(
                    resume.title, resume.writer_name, resume.email,
                    resume.phone_number, resume.description)

                if total_length < 400 :
                    return JsonResponse({'message':f'현재 글자수 {total_length}자'}, status = 202)
                
                resume.completion_status = "작성 완료"
                resume.save()
                return JsonResponse({'message':'작성 완료'}, status = 200)
        
            except ValidationError as v : 
                return JsonResponse({'message': f"{v}"}, status = 401)
        return JsonResponse({"message" : "INVALID ACCESS"}, status=400)  