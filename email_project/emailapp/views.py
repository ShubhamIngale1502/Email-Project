from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializer import EmpSerializer
from .models import Employee
import logging
from  rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .utils import EmailThread
from django.conf import settings

logger = logging.getLogger('mylogger')

@api_view(http_method_names=['POST','GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_emp(request):
    if request.method == 'POST':
        try:
            serializer = EmpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('The Employee is created')
            user_email = request.data.get('email')
            subject = "Test Email"
            message = 'User created SuccesFully'
            if user_email :
                EmailThread(
                    subject = subject,
                    message = message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list = [user_email]
                ).start()
                return Response(data={'details':'Email Send Succesfully'})
            return Response(data=serializer.data, status=201)
        except:
            logger.error("This Data seved with errors")
            return Response(data=serializer.errors, status=400)

    if request.method == 'GET':
        try:
            obj = Employee.objects.all()
            serializer = EmpSerializer(obj, many=True)
            logger.info('Employee data is fetched succesfully')
            return Response(data=serializer.data, status=200)
        except:
            logger.error("This Data fetched with errors")
            return Response(data=serializer.errors, status=400)
        
@api_view(http_method_names=['GET','PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def details(request,pk):
    
    obj = get_object_or_404(Employee,pk=pk)
    if request.method == 'GET':
        try:
            serializer = EmpSerializer(obj)
            logger.info('Employee data is fetched succesfully')
            return Response(data=serializer.data, status=200)
        except:
            logger.error("This Data fetched with errors")
            return Response(data={'details':'It has Some Errors'},status=400)

    if request.method == 'PUT':
        try:
            serializer = EmpSerializer(data=request.data, instance=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Employee Data Updated Succesfully')
            user_email = request.data.get('email')
            subject = "Test Email"
            message = 'User Updated SuccesFully'
            if user_email :
                EmailThread(
                    subject = subject,
                    message = message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list = [user_email]
                ).start()
                return Response(data={'details':'Email Send Succesfully'})
            return Response(data=serializer.data, status=200)
        except:
            logger.error("This Updated with errors")
            return Response(data={'details':'It has Some Errors'},status=400)
        
    if request.method == 'PATCH':
        try:
            serializer = EmpSerializer(data=serializer.data, instance=obj,partial = True)
            serializer.is_valid()
            serializer.save()
            logger.info('Employee Data Updated Succesfully')
            return Response(data=serializer.data, status=200)
        except:
            logger.error("This Updated with errors")
            return Response(data={'details':'It has Some Errors'},status=400)
    
    if request.method == 'DELETE':
        try:
            obj.delete()
            logger.info('Employee Deleted Successfully')
            user_email = request.data.get('email')
            subject = "Test Email"
            message = 'User Deleted SuccesFully'
            if user_email :
                EmailThread(
                    subject = subject,
                    message = message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list = [user_email]
                ).start()
                return Response(data={'details':'Email Send Succesfully'})
            return Response(data=None, status=204)
        except:
            logger.info('Employee deletinng having some errors')
            return Response(data={'details':'No Content'}, status=204)
            
