from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializers,UserloginSerializer
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

'''this is generating token manually'''
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
'''this is to register the user '''
class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format = None):
        serializer = UserRegistrationSerializers(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return Response({'msg':'Registration sucessfull'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


'''this is to login user '''
from django.contrib.auth import authenticate,login
class LoginView(APIView):
    renderer_classes=[UserRenderer]

    def post(self,request,format = None):
        serializer = UserloginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            # login(request,user)
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':"login sucessfull"},status=status.HTTP_200_OK)
        return Response({'errors':{'non_field_error':['email or password didnot match ']}},status=status.HTTP_404_NOT_FOUND)
    


'''how to see the user profile '''
from .serializers import UserProfileViewSerializer
from rest_framework.permissions import IsAuthenticated
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format = None):
        serializer = UserProfileViewSerializer(request.user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)



'''this is to change the password with out email address'''
from .serializers import ChangepasswordSerializer
class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = ChangepasswordSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({ 'msg':'password change sucessfully '},status=status.HTTP_200_OK)



'''this is to send email address '''
from .serializers import EmailPasswordSerializer
class EmailPasswordView(APIView):
    renderer_classes = [UserRenderer]

    def post(self,requset,format=None):
        serializer = EmailPasswordSerializer(data= requset.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'please check email to change your password '},status=status.HTTP_200_OK)



'''this is to change password with email after email address is sent'''
from .serializers import ResetSerializer
class ResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format = None):
        serializer = ResetSerializer(data=request.data,context={'uid':uid,'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({ 'msg':'password change sucessfully '},status=status.HTTP_200_OK)


'''this is to logout the user '''
from rest_framework import generics
from .serializers import LogoutSerializer
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializers = LogoutSerializer(data = request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(status=status.HTTP_200_OK)


