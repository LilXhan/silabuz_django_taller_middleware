from ipware import get_client_ip
from django.http import HttpResponse
from django.http import Http404


BLACK_LIST = ['127.0.0.1']

def ip_is_valid(get_response):
    # ...
    def middleware(request):
        # Codigo que se ejecutara llamando a la vista
        print('Hola mundo desde un Middleware!')

        # Get ip

        ip, is_routable = get_client_ip(request)

        response = get_response(request)

        if ip in BLACK_LIST:
            return HttpResponse('Bad request', status=404)
        
        return response

        # Codigo que se ejecutara desde del llamado a la vista
    
    return middleware


class IpIsValid:
    
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):

        ip, is_routable = get_client_ip(request)

        response = self.get_response(request)

        if ip in BLACK_LIST:
            raise Http404

        return response