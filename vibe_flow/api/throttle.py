from datetime import date
from rest_framework.throttling import BaseThrottle
from .models import PrivateG ,  RateProfile


class CreatingPrivateGroupThrottle(BaseThrottle) :       
       def allow_request(self, request, view):
              activate_user = request.user.accounts
              today = date.today()
              group = PrivateG.objects.filter(owner=activate_user , created_at__date=today)
              if group :
                     return False
              return True

class OneTimeProfileRate(BaseThrottle) :
       def allow_request(self, request, view):
              user = request.user.accounts
              profile_id = request.data.get('profile')
              if profile_id is not None :
                     rate = RateProfile.objects.filter(rater=user , profile = profile_id)
                     if rate :
                            return False
              return True       