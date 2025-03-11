from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import generics , permissions
from rest_framework.decorators import api_view
from .models import (
       User , Account , Post ,
       PostLike , Comment , MarketPlace ,
       Public , PrivateG ,FriendRequest ,
       RateProfile , Notification , Message
       )

from .serializer import (
       RegistrationSerializer ,  AccountSerializer ,
       PostSerializer , PostLikeSerializer ,
       CommentSerializer , MarketPlaceSerializer , 
       JoinPrivateGroupSerializer , JoinPublicGroupSerializer ,
       PublicGroupSerializer , PrivateGroupSerializer , 
       CreatePostInPrivateGroupSerializer , CreatePostInPublicGroupSerializer ,
       PrivateSerializer , PublicSerializer ,
       SendFriendRequestSerializer , ProfilerateSerializer,
       NotificationSerializer , MessageSerializer
)

from .throttle import CreatingPrivateGroupThrottle , OneTimeProfileRate
from .permission import (
       ProfilePermission , PrivateGroupPermission ,
       PermissionToUpdatePrivateGroup,PermissionModifyComment,
       
       )
from django.shortcuts import redirect , get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from .utils import generate_qr_code
import random

def users_code() :
       list = ["fe9","ew5"]
       return random.choice(list)

@api_view(['POST'])
def create_user_and_send_email(request):
    if request.method == 'POST':
       serializer = RegistrationSerializer(data=request.data)
       if serializer.is_valid():

           user = serializer.save()
           subject = f'Welcome to Our Platform your code is{users_code()}'
           message = f'Hello {user.username},\n\nThank you for registering with us!'
           from_email = settings.EMAIL_HOST_USER  

           recipient_list = [user.email]  
           user_data = {
                  "username" : user.username,
                  "email" : user.email,
           }
          
           qr = generate_qr_code(user_data)
           
           try:
              send_mail(subject, message, from_email, recipient_list)
              return Response({
              'message': 'User created and welcome email sent successfully!'
              }, status=status.HTTP_201_CREATED)
           except Exception as e: 
              return Response({
              'message': f'User created, but email could not be sent. Error: {str(e)}'
              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthUsersView(APIView) :
       def get(self,request, *args,**kwargs) :
              user = self.request.user
              return Response(f"{user}")

class UserProfileEndPoint(APIView) :
       permission_classes = [ProfilePermission]
       def get(self,request,*args,**kwargs):
              user        = self.request.user
              account     = get_object_or_404(Account,user=user)
              serializer  = AccountSerializer(account , many=False)
              return Response(serializer.data , status=status.HTTP_200_OK)
              
              
class UpdateProfileInformations(generics.UpdateAPIView) :
       serializer_class   = AccountSerializer
       permission_classes = [ProfilePermission]
       queryset           = Account.objects.all()
       lookup_field       = "pk"

class PostEndPoint(GenericAPIView ,CreateModelMixin) :
       # permission_classes = [permissions.IsAuthenticated]
       serializer_class   = PostSerializer
       def post(self , request , *args , **kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
                     author       = self.request.user
                     title        = serializer.validated_data["title"]
                     descriptions = serializer.validated_data["descriptions"]
                     try :
                            account = Account.objects.get(user=author)
                     except Account.DoesNotExist :
                            return Response("error")
                     
                     post                = Post.objects.create(
                            title        = title,
                            descriptions = descriptions , 
                            account      = account
                     )
                     post.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              return Response(serializer.errors , status=status.HTTP_406_NOT_ACCEPTABLE)

class PostListEndPoint(generics.ListAPIView) :
       serializer_class   = PostSerializer
       queryset           = Post.objects.all()
       permission_classes = [permissions.IsAuthenticated]

class PostDetailEndpoint(generics.RetrieveUpdateAPIView) :
       serializer_class   = PostSerializer
       queryset           = Post.objects.all()
       lookup_field       = "pk"              
       permission_classes = [permissions.IsAuthenticated]

class DeletePostEndpoint(generics.DestroyAPIView) :
       serializer_class   = PostSerializer
       queryset           = Post.objects.all()
       lookup_field       = "pk"              
       permission_classes = [permissions.IsAuthenticated]


class LikePostEndPoint(GenericAPIView , CreateModelMixin) :
       serializer_class   = PostLikeSerializer
       permission_classes = [permissions.IsAuthenticated]
       def post(self,request,*args,**kwargs) :
              data = request.data
              serializer = self.get_serializer(data=data)

              if serializer.is_valid(raise_exception=True) :
                     post    = serializer.validated_data["post"]
                     account = serializer.validated_data["account"]

                     post_like_filter = PostLike.objects.filter(account=account)

                     if post_like_filter :
                            post_like_filter.delete()
                            return Response("u remove the like")
                     
                     like           = PostLike.objects.create(
                            post    = post ,
                            account = account, 
                     )
                     like.save()
                     return Response({"msg": f"congrats ...{account.user.username} you like post of"}) 
              return Response(serializer.errors , status=status.HTTP_404_NOT_FOUND)
                     
class CommentsEndPoint(GenericAPIView,CreateModelMixin):
       serializer_class = CommentSerializer
       permission_classes = [permissions.IsAuthenticated]
       def post(self,request ,*args ,**kwargs) :
              serializer = self.get_serializer(data = request.data)
              if serializer.is_valid() :
                     try :
                            post    = serializer.validated_data["post"]
                            account = serializer.validated_data["account"]
                            content = serializer.validated_data["content"]
                     except :
                            return Response("error..")
                     
                     comments       = Comment.objects.create(
                            post    = post ,
                            account = account,
                            content = content
                     )
                     comments.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              
              return Response({"error message" : serializer.errors} , status=status.HTTP_400_BAD_REQUEST)
                     
class RUD_Comment(generics.RetrieveUpdateDestroyAPIView) :
       serializer_class   = CommentSerializer
       queryset           = Comment.objects.all()
       lookup_field       = "pk"
       permission_classes = [PermissionModifyComment]

class MarketPlaceEndpoint(GenericAPIView,CreateModelMixin) :
       serializer_class   = MarketPlaceSerializer
       permission_classes = [permissions.IsAuthenticated]

       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              user       = self.request.user
              if serializer.is_valid() :
                     try :
                            seller_account = Account.objects.get(user=user)
                     except Account.DoesNotExist :
                            return Response("error")
                     
                     seller               = serializer.validated_data["seller"]
                     product_name         = serializer.validated_data["product_name"]
                     product_image        = serializer.validated_data["product_image"]
                     product_price        = serializer.validated_data["product_price"]
                     product_informations = serializer.validated_data["product_informations"]

                     market_place                = MarketPlace.objects.create(
                            seller               = seller , 
                            product_name         = product_name ,
                            product_image        = product_image,
                            product_price        = product_price , 
                            product_informations = product_informations
                     )

                     market_place.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
       
              return Response(serializer.errors , status=status.HTTP_404_NOT_FOUND)
       
class MarketProductEndpoint(generics.ListAPIView) :
       permission_classes = [permissions.IsAuthenticated]
       serializer_class   = MarketPlaceSerializer
       queryset           = MarketPlace.objects.all()

class SingleProduct(generics.RetrieveUpdateDestroyAPIView) :
       permission_classes = [permissions.IsAuthenticated]
       serializer_class   = MarketPlaceSerializer
       queryset           = MarketPlace.objects.all()
       lookup_field       = "pk"

class PrivateGroupEndPoint(GenericAPIView, CreateModelMixin) :
       serializer_class   = JoinPrivateGroupSerializer
       permission_classes = [permissions.IsAuthenticated]
       queryset           = PrivateG.objects.all()
       
       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
 
                     active_account = self.request.user.accounts
                     group_id       = serializer.validated_data["group_id"]
                     code           = serializer.validated_data["code"]
                     group          = get_object_or_404(PrivateG , id=group_id)

                     if group.code == code and active_account not in group.members.all() :
                            group.members.add(active_account)
                            group.save()
                            return Response("congrats.. u join the groupe" , status=status.HTTP_202_ACCEPTED)
                     
                     return Response("invalid code.." , status=status.HTTP_404_NOT_FOUND)
       
              return Response("error" , status=status.HTTP_404_NOT_FOUND)
       def get(self , request, *args, **kwargs) :
              # serializer = self.get_serializer()
              pass

class PublicGroupEndPoint(GenericAPIView, CreateModelMixin) :
       serializer_class   = JoinPublicGroupSerializer
       permission_classes = [permissions.IsAuthenticated]
       def post(self,request,*args,**kwargs) :
              serializer  = self.get_serializer(data=request.data)
              if serializer.is_valid() : 
                     active_account = self.request.user.accounts
                     group_id       = serializer.validated_data["group_id"]
                     group          = get_object_or_404(Public , id=group_id)
                     group.members.add(active_account)
                     group.save()
              
                     return Response("you Join" , status=status.HTTP_202_ACCEPTED)
       
              return Response("error" , status=status.HTTP_404_NOT_FOUND)

class PrivateGroupList(generics.ListAPIView) :
       serializer_class   = PrivateGroupSerializer
       queryset           = PrivateG.objects.all()              
       permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PublicGroupList(generics.ListAPIView) :
       serializer_class   = PublicGroupSerializer
       queryset           = Public.objects.all()                
       permission_classes = [permissions.IsAuthenticatedOrReadOnly]
 

class CreatePostInPrivateGroup(GenericAPIView,CreateModelMixin) :
       serializer_class   = CreatePostInPrivateGroupSerializer 
       permission_classes = [PrivateGroupPermission]
      
       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
                     
                     account      = self.request.user.accounts
                     title        = serializer.validated_data["title"]
                     image        = serializer.validated_data["image"]
                     private      = serializer.validated_data["private"]
                     descriptions = serializer.validated_data["descriptions"]
 
                     post = Post.objects.create(
                            title        = title,
                            image        = image,
                            private      = private,
                            descriptions = descriptions,
                            account      = account
                     )
                     post.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
      
              return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class CreatePostInPublicGroup(GenericAPIView,CreateModelMixin) :
       serializer_class   = CreatePostInPublicGroupSerializer 
       permission_classes = [PrivateGroupPermission]
       def post(self,request,*args,**kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
                     account      = self.request.user.accounts
                     title        = serializer.validated_data["title"]
                     image        = serializer.validated_data["image"]
                     private      = serializer.validated_data["private"]
                     descriptions = serializer.validated_data["descriptions"]
                     post                = Post.objects.create(
                            title        = title,
                            image        = image,
                            private      = private,
                            descriptions = descriptions,
                            account      = account
                     )
                     post.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class CreatePrivateGroup(GenericAPIView , CreateModelMixin) :
       serializer_class = PrivateSerializer
       # permission_classes = [permissions.IsAuthenticated]
       throttle_classes = [CreatingPrivateGroupThrottle]
       def post(self, request , *args , **kwargs) :
              serializer = self.get_serializer(data=request.data)

              if serializer.is_valid() :
                     owner = self.request.user.accounts
                     code  = serializer.validated_data["code"]

                     private = PrivateG.objects.create(owner=owner,code=code)
                     private.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              
              return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class UpdatePrivateGroup(generics.UpdateAPIView) :
       serializer_class   = PrivateSerializer
       permission_classes = [PermissionToUpdatePrivateGroup]
       queryset           = PrivateG.objects.all()
       lookup_field       = "pk"


class DeletePrivateGroup(generics.DestroyAPIView) :
       serializer_class   = PrivateSerializer
       permission_classes = [PermissionToUpdatePrivateGroup]
       queryset           = PrivateG.objects.all()
       lookup_field       = "pk"

class CreatePublicGroup(GenericAPIView , CreateModelMixin) :
       
       serializer_class   = PublicSerializer
       permission_classes = [permissions.IsAuthenticated]
       throttle_classes   = [CreatingPrivateGroupThrottle]
       
       def post(self, request , *args , **kwargs) :
              serializer = self.get_serializer(data=request.data)

              if serializer.is_valid() :
                     owner   = self.request.user.accounts
                     private = PrivateG.objects.create(owner=owner)
                     private.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              
              return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
       
class UpdatePublicGroup(generics.UpdateAPIView) :
       serializer_class   = PublicSerializer
       permission_classes = [PermissionToUpdatePrivateGroup]
       queryset           = Public.objects.all()
       lookup_field       = "pk"

       
class DeletePublicGroup(generics.DestroyAPIView) :
       serializer_class   = PublicSerializer
       permission_classes = [PermissionToUpdatePrivateGroup]
       queryset           = Public.objects.all()
       lookup_field       = "pk"

class FriendRequestEndpoint(APIView) :
       permission_classes = [ProfilePermission]
       def get(self , request, *args , **kwargs) :
              account = self.request.user.accounts
              print(account)
              queryset   = FriendRequest.objects.filter(reciver=account , status="pending")
              serializer = SendFriendRequestSerializer(queryset , many=True)
              return Response(serializer.data , status=status.HTTP_200_OK)


class AcceptFriendRequest(GenericAPIView , CreateModelMixin):
       permission_classes = [permissions.IsAuthenticated , ProfilePermission]
       def post(self,request , friend_request_id) :
              
              friend_id = get_object_or_404(FriendRequest , id=friend_request_id)

              friend_id.status = "accept"
              friend_id.save()
              return Response(f"{friend_id.sender.user.username} add to you frined list..",
                            status=status.HTTP_202_ACCEPTED)
       
class DeclineFriendRequest(GenericAPIView , CreateModelMixin):
       permission_classes = [permissions.IsAuthenticated , ProfilePermission]
       def post(self,request , friend_request_id) :
              
              friend_request_id = get_object_or_404(FriendRequest , id=friend_request_id)

              friend_request_id.status = "decline"
              friend_request_id.delete()
              friend_request_id.save()
              return Response(f"friend request deleted..",
                            status=status.HTTP_202_ACCEPTED)

class AccountFriendList(APIView) :
       permission_classes = [permissions.IsAuthenticated , ProfilePermission]
       def get(self , request , *args , **kwargs) :
              friend_list = FriendRequest.objects.filter(reciver = self.request.user.accounts ,status="accept")
              serializer  = SendFriendRequestSerializer(friend_list , many=True)
              return Response(serializer.data , status=status.HTTP_200_OK)

class RateProfileEndPoint(GenericAPIView , CreateModelMixin) :
       serializer_class = ProfilerateSerializer
       throttle_classes = [OneTimeProfileRate]
       def post(self , request , *args , **kwargs) :
              serializer = self.get_serializer(data=request.data)
              if serializer.is_valid() :
                     profile           = serializer.validated_data["profile"] 
                     rate_value        = serializer.validated_data["rate_value"]

                     rate_profile      = RateProfile.objects.create(
                            rater      = self.request.user.accounts.rater , 
                            profile    = profile , 
                            rate_value = rate_value
                     )
                     rate_profile.save()

                     return Response(serializer.data , status=status.HTTP_201_CREATED)              
              return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class WhoRateMyProfile(APIView) :
       def get(self , request , *args,**kwargs) :
              profile       = self.request.user.accounts
              rated_profile = RateProfile.objects.filter(profile=profile)
              serializer    = ProfilerateSerializer(rated_profile , many=True)
              return Response(serializer.data)

class NotificationView(APIView) :
       permission_classes = [ProfilePermission]
       def get(self , request) :
              active_user  = request.user.accounts
              notification = Notification.objects.filter(account=active_user,mark_as_read=False)
              notify_count = notification.count()
              # serializer   = NotificationSerializer(notification , many=True)
              return Response(
                     {
                            "notification" : NotificationSerializer(notification , many=True).data,
                            "notification_count" : notify_count
                     } , 
                     status = status.HTTP_200_OK
              )

class NotificationDetail(APIView) :
       def get(self,request , notify_id) :
              notification = get_object_or_404(Notification , id=notify_id)
              notification.mark_as_read = True
              notification.save()
              serializer   = NotificationSerializer(notification , many=False)
              return Response(serializer.data , status=status.HTTP_200_OK)


class InboxMessagesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
       
       active_user = request.user.accounts 
       recived_messages = Message.objects.filter(message_reciver=active_user)
       sent_messages    = Message.objects.filter(message_sender=active_user)
       
       return Response(
              {
              "recived_messages" : MessageSerializer(recived_messages , many=True).data,
              "sent_messages" : MessageSerializer(sent_messages , many=True).data
       },
       status=status.HTTP_202_ACCEPTED
       )

class SendMessageAPIView(APIView) :
       permission_classes = []
       def post(self,request) :
              serializer = MessageSerializer(data=request.data)
              message_sender = self.request.user.accounts
              if serializer.is_valid() :
                     message_reciver = serializer.validated_data["message_reciver"]
                     message_content = serializer.validated_data["message_content"]
                     message = Message.objects.create(
                            message_sender  = message_sender,
                            message_reciver = message_reciver,
                            message_content = message_content
                     )
                     message.save()
                     return Response(serializer.data , status=status.HTTP_201_CREATED)
              return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class RetrieveMessageAPIView(APIView):
       permission_classes = [permissions.IsAuthenticated]
       def get(self, request, message_id):
              active_user = request.user.accounts
              message = get_object_or_404(Message, id=message_id)

              if message.message_sender == active_user or message.message_receiver == active_user:
                     serializer = MessageSerializer(message)
                     return Response(serializer.data, status=status.HTTP_200_OK)
              else:
                     return Response({"error": "You do not have permission to view this message."}, status=status.HTTP_403_FORBIDDEN)

class DeleteConversationMessagesAPIVIew(APIView):
       permission_classes = [permissions.IsAuthenticated]
       def delete(self, request, message_id):
              active_user = request.user.accounts
              message     = get_object_or_404(Message, id=message_id)

              if message.message_sender == active_user or message.message_receiver == active_user:
                     message.delete()
                     return Response({"message": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
              else:
                     return Response(
                            {"error": "You do not have permission to delete this message."}, status=status.HTTP_403_FORBIDDEN) 
