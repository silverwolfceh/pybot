import requests
import urllib3
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



class NoVerifySession(requests.Session):
    def send(self, request, **kwargs):
        kwargs['verify'] = False
        return super().send(request, **kwargs)

def create_req_session():
    session = NoVerifySession()
    return session