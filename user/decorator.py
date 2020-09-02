import bcrypt
import jwt 

from django.http           import JsonResponse

from wwe.settings         import SECRET_KEY, ALGORITHM 
from .models              import UserAccount

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.headers.get('Authorization', None) :
            return JsonResponse({"message" : "INVALID_SIGNIN"}, status=401)

        try:
            access_token = request.headers.get('Authorization', None)
            
            if access_token :                 
                payload         = jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM)
                user            = UserAccount.objects.get(id = payload['user_id'])
                request.user    = user
                return func(self, request, *args, **kwargs)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status = 401)       
        
        except UserAccount.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
    return wrapper