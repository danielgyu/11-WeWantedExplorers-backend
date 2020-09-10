import json
import bcrypt
import jwt
import traceback
import requests
from json.decoder           import JSONDecodeError

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from wwe.settings           import ALGORITHM, SECRET_KEY
from .models                import (
    UserAccount, 
    UserInformation, 
    MatchUpInformation,
    JobSkill, 
    Recomender, 
    CompanyException,
    SuggestionStatus, 
    ApplicationStatus
    )    
from .validator             import (
    Validate_email, 
    Validate_password, 
    Validate_phonenumber
    )
from .decorator             import signin_decorator
from position.models        import Position
from company.models         import Company

class EmailCheckerView(View):
    def post(self, request):
        data = json.loads(request.body)
        try :
            if UserAccount.objects.filter(email=data['email']).exists() :
                return JsonResponse({'message':'SignIn'}, status = 202)
            user = UserAccount(
                email         = data['email'],
                platform_type = 'Wanted'
                )
            user.full_clean()
        
        except ValidationError as v : 
            tb = traceback.format_exc()
            return JsonResponse({'message':tb}, status = 400)

        except KeyError :
            return JsonResponse({'message':'KEY ERROR'}, status = 401)

        return JsonResponse({'message':'SignUp'}, status = 201)
        
class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)
        try :
            user, create = UserAccount.objects.get_or_create(
                email=data['email'],
                platform_type='Wanted')
            userinfo = UserInformation(
                name         = data['name'],
                phone_number = data['phone_number'],
                password     = data['password'],
                user_account = user
            )
            userinfo.full_clean() 
            userinfo.password  = bcrypt.hashpw(
                userinfo.password.encode(
                    'utf-8'),bcrypt.gensalt()).decode('utf-8')            
            userinfo.save()
        except ValidationError as v : 
            tb = traceback.format_exc()
            return JsonResponse({'message':tb}, status = 400)

        except KeyError :
            return JsonResponse({'message':'KEY ERROR'}, status = 401)
        
        except json.JSONDecodeError : 
            return JsonResponse({'message':'INVALID_JSON'}, status=406) 

        return JsonResponse({'message':'SUCCESS'}, status = 200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try :
            if UserAccount.objects.prefetch_related('userinfo').filter(email = data['email']).exists() :
                user = UserAccount.objects.get(email = data['email']).userinfo.first()
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode(
                        {'user_id': user.id}, 
                        SECRET_KEY, algorithm = ALGORITHM)
                    token = token.decode('utf-8')
                    return JsonResponse({'message':"SUCCESS", "token":token}, status = 200)
            return JsonResponse({'message':'PASSWORD_ERROR'}, status = 400) 
        
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status = 401) 

class GoogleSignInView(View):
    def get(self, request):
        Google_token = request.headers.get('Authorization')
        response     = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?access_token={Google_token}")
        user         = response.json()
        google_email = user.get('email')
        if UserAccount.objects.filter(email = google_email).exists():
            user = UserAccount.objects.get(email = google_email)
            token = jwt.encode(
                    {'user_id': user.id}, 
                    SECRET_KEY, algorithm = ALGORITHM)
            access_token = token.decode('utf-8')
            return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status = 200)
        return JsonResponse({'message': google_email}, status = 202)
        
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = UserAccount.objects.create(
                email         = data['email'],
                platform_type ='Google'
                )
            userinfo = UserInformation(
                name         = data['name'],
                phone_number = data['phone_number'],
                password     = 'googlepassword',
                user_account = user
                )
            userinfo.full_clean()            
            userinfo.save()
        except ValidationError as v : 
            tb = traceback.format_exc()
            return JsonResponse({'message':tb}, status = 400)

        except KeyError :
            return JsonResponse({'message':'KEY ERROR'}, status = 401) 
        
        except json.JSONDecodeError : 
            return JsonResponse({'message':'INVALID_JSON'}, status=406) 

        return JsonResponse({'message':'SignUp completed'}, status = 200)

class ApplicationView(View):
    @signin_decorator
    def get(self, request):
        user = UserAccount.objects.prefetch_related("userinfo").get(id=request.user.id)
        resume_packs = user.userinfo.first().resume.all()
        
        body = {
            "applicant_information":{
                "name"         : user.userinfo.first().name,
                "email"        : user.email,
                "phonenumber"  : user.userinfo.first().phone_number,
                "recomender"   : "선택사항"},
            
            "attatchment":[{
                "id"                : resume.id,
                "languae"           : "한국어",
                "title"             : resume.title,
                "created_at"        : resume.created_at,
                "completion_status" : resume.completion_status,
            } for resume in resume_packs]}
        return JsonResponse(body, status=200)

class ApplicationStatusView(View):
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user.userinfo.first()
        position = Position.objects.select_related(
            "company").get(id=data['position_id'])

        if not ApplicationStatus.objects.filter(
            user_information_id=user, 
            position_id=data['position_id']).exists():
            ApplicationStatus.objects.create(
                company          = position,
                position         = position,
                logo_url         = position,
                process_status   = "접수",
                is_compensation  = True,
                user_information = user
            )
            return JsonResponse({'message' : 'DONE'}, status = 200)
        return JsonResponse({'message' : 'INVALID'}, status = 401)

    @signin_decorator
    def get(sef,request):
        try : 
            data = json.loads(request.body)
            user = request.user.userinfo.first()
            applications = ApplicationStatus.objects.select_related(
                "company", "position", "logo_url"
            ).filter(user_information=user).all()

            body = {
                "process" : {
                    "total"  : applications.count(),
                    "hired"  : applications.filter(process_status="채용 완료").count(),
                    "pass"   : applications.filter(process_status="서류 통과").count(),
                    "accept" : applications.filter(process_status="접수").count(),
                    "reject" : applications.filter(process_status="불합격").count()
                },
                "application_status":[
                    {
                        "company"         : datum.position.company.name, 
                        "position"        : datum.position.title,
                        "logo_url"        : datum.position.company.logo_url,
                        "applicant_name"  : user.name,
                        "created_at"      : datum.created_at,
                        "result"          : "진행중", 
                    }for datum in applications]}
            return JsonResponse(body, status = 200)

        except KeyError :
            return JsonResponse({'message':'KEY ERROR'}, status = 401)