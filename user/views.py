import json
import bcrypt
import jwt

from django.shortcuts       import render
from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Prefetch
from django.core.exceptions import ValidationError

from .models                import UserAccount, UserInformation, MatchUpInformation
from .models                import JobSkill, Recomender, CompanyException
from .models                import SuggestionStatus, ApplicationStatus    