from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import(
   Account , Post , PostLike , Comment ,
   MarketPlace , Public , PrivateG , FriendRequest ,
   RateProfile , User , Notification , Message
)

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
       model = User
       fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def validate(self, data):
       if data['password'] == None:
            raise serializers.ValidationError({"password": "Empty password.. chose a strong password"})
      #  if  (data["password"].isupper() or data["password"].islower() or data["password"].isdigit() ) :
      #    raise serializers.ValidationError({"message":"password should contain Maj and Mins , special caracters and number"})
       return data

    def create(self, validated_data):
       password = validated_data.pop('password')
       user = User.objects.create_user(**validated_data, password=password)
       return user


class AccountSerializer(serializers.ModelSerializer) :
    class Meta :
       model = Account
       fields =  ["user","profile_image","bio","created","posts","notify" , "message_sender" , "message_reciver"]

class PostSerializer(serializers.ModelSerializer) :
    
   class Meta :
      model = Post
      fields = ["title","image","descriptions","created_at","account","likes","comments"]


class PostLikeSerializer(serializers.ModelSerializer) :
   class Meta :
      model = PostLike
      fields = ["post","account"]


class CommentSerializer(serializers.ModelSerializer) :
   class Meta :
      model  = Comment
      fields = ["post","account","content",] 

   def validate(self , data) :
      if data["content"] == "" :
         raise serializers.ValidationError("u can't post an empty comment")
      return data

class MarketPlaceSerializer(serializers.ModelSerializer) :
   class Meta :
      model  = MarketPlace
      fields = ["seller","product_name","product_image","product_price","product_informations"]

class PrivateGroupSerializer(serializers.ModelSerializer) :
   class Meta :
      model = PrivateG
      fields = ["owner","members","posts"]

class PublicGroupSerializer(serializers.ModelSerializer) :
   class Meta :
      model = Public
      fields = ["owner","members"]


class JoinPrivateGroupSerializer(serializers.Serializer) :
   group_id = serializers.IntegerField()
   code = serializers.CharField()
     
class JoinPublicGroupSerializer(serializers.Serializer) :
   group_id = serializers.IntegerField()

class CreatePostInPrivateGroupSerializer(serializers.ModelSerializer) :
   class Meta :
      model = Post
      fields =[
         "title",
         "image",
         "descriptions",
         "private",
         "account"
         ]

class CreatePostInPublicGroupSerializer(serializers.ModelSerializer) :
   class Meta :
      model = Post
      fields = [
         "title",
         "image",
         "descriptions",
         "private",
         "account"
         ]
      
class PrivateSerializer(serializers.ModelSerializer) :
   class Meta :
      model  = PrivateG
      fields = "__all__"

class PublicSerializer(serializers.ModelSerializer) :
   class Meta :
      model = Public
      fields = "__all__"   

class SendFriendRequestSerializer(serializers.ModelSerializer) :
   class Meta :
      model  = FriendRequest
      fields = ["sender","reciver","status"]

class ProfilerateSerializer(serializers.ModelSerializer) :
   # rate_total = serializers.SerializerMethodField()
   class Meta :
      model = RateProfile
      fields = [
         "rater","profile","rate_value" 
      ]

   # def get_rate_total(self ,obj) :
   #    return obj.rate_total()
   
   def validate(self, data):

      if data["rate_value"] > 10 or data["rate_value"] < 0 :
         raise serializers.ValidationError("rate value must be greater than 0 nd less than or equal to 10")

      return data      

class NotificationSerializer(serializers.ModelSerializer) :
   class Meta :
      model = Notification
      fields = [
         "account",
         "created_at",
         "message",
         "mark_as_read"
         ]
      
class MessageSerializer(serializers.ModelSerializer) :
   class Meta :
      model  = Message
      fields = [ "message_sender","message_reciver","content","timestamp"  ]
      read_only_fields = ["content", "timestamp"]

   def validate(self, data):
      if data["content"] == "" :
         return serializers.ValidationError("Message Field Is Required")
      
      return data