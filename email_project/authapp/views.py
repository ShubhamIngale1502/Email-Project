from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer
import logging

logger = logging.getLogger('mylogger')
@api_view(http_method_names=['POST'])
def user(request):
    if request.method == 'POST':
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            logger.info('The Employee is created')
            return Response(data=serializer.data, status=201)
        except:
            logger.error("This Data seved with errors")
            return Response(data=serializer.errors, status=400)
