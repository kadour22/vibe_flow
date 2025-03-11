from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

urlpatterns = [
       # User urls
       path("register/" , views.create_user_and_send_email , name="send-mail"),
       path("token/" , TokenObtainPairView.as_view()),
       path("token/refresh/" ,TokenRefreshView.as_view()),
       path("profile/" , views.UserProfileEndPoint.as_view()),
       path("profile-update/<int:pk>/" , views.UpdateProfileInformations.as_view()),
       # post urls
       path("post-list/" , views.PostListEndPoint.as_view()),
       path("post/" , views.PostEndPoint.as_view()),
       path("post-detail/<int:pk>/" , views.PostDetailEndpoint.as_view()),
       path("like/" , views.LikePostEndPoint.as_view()),
       # comments urls 
       path("add_comment/" , views.CommentsEndPoint.as_view()),
       path("comment/<int:pk>/" , views.RUD_Comment.as_view()),
       # market place urls
       path("add_product_market/", views.MarketPlaceEndpoint.as_view()),
       path("market_products_list/" , views.MarketProductEndpoint.as_view()),
       path("market/product/<int:pk>/" , views.SingleProduct.as_view()),
       # group urls
       path("join-private-group/" , views.PrivateGroupEndPoint.as_view()),
       path("join-public-group/" , views.PublicGroupEndPoint.as_view()),
       path("private-group-list/" , views.PrivateGroupList.as_view()),
       path("public-group-list/" , views.PublicGroupList.as_view()),
       path("create-private-post/" , views.CreatePostInPrivateGroup.as_view()),
       path("create-public-post/" , views.CreatePostInPublicGroup.as_view()),
       path("create-private-group/" , views.CreatePrivateGroup.as_view()),
       path("update-private-group/<int:pk>/" , views.UpdatePrivateGroup.as_view()),
       path("delete-private-group/<int:pk>/" , views.DeletePrivateGroup.as_view()),
       path("create-public-group/" , views.CreatePublicGroup.as_view()),
       path("update-public-group/<int:pk>/" , views.UpdatePublicGroup.as_view()),
       path("delete-public-group/<int:pk>/" , views.DeletePublicGroup.as_view()),
       # friend requests logic
       path("friend-request-list/" , views.FriendRequestEndpoint.as_view()),
       path("accept-friend-request/<int:friend_request_id>/" , views.AcceptFriendRequest.as_view()),
       path("decline-friend-request/<int:friend_request_id>/" , views.DeclineFriendRequest.as_view()),
       path("friends-list/" , views.AccountFriendList.as_view()),
       # profile rate
       path("rate-profile/", views.RateProfileEndPoint.as_view()),
       path("who-rate/" , views.WhoRateMyProfile.as_view()),
       # Notifications
       path("notification/" , views.NotificationView.as_view()), 
       path("notification/<int:notify_id>/" , views.NotificationDetail.as_view()), 
       # Messages
       path("messages/inbox/" , views.InboxMessagesAPIView.as_view()),
       path("messages/send-message/" , views.InboxMessagesAPIView.as_view()),
       path("messages/message/<int:message_id>/" , views.InboxMessagesAPIView.as_view()),
       path("messages/delete/<int:message_id>/" , views.InboxMessagesAPIView.as_view()),
]
