from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
import qrcode
import json
from .models import Account , Notification , User , PostLike , Message


@receiver(post_save , sender=User)
def create_user_account(sender, instance, created, **kwargs) :
    if created :
        account = Account.objects.create(user=instance)
        account.save()

@receiver(post_save , sender=Account)
def notify_accounts(sender , instance , created , **kwargs) :
    if created :
        skipped_account = Account.objects.exclude(id=instance.id)
        notify          = Notification.objects.create(message=f"new user join")

        notify.account.set(skipped_account)

@receiver(post_save, sender=PostLike)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        post       = instance.post
        liker      = instance.account
        post_owner = post.account

        # Create a notification
        notification_message = f"{liker.user.username} liked your post: {post.title}"
        notification         = Notification.objects.create(message=notification_message)
        notification.account.add(post_owner)
        notification.save()

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        sender_account   = instance.sender
        receiver_account = instance.receiver

        # Create a notification
        notification_message = f"{sender_account.user.username} sent you a message"
        notification         = Notification.objects.create(message=notification_message)
        notification.account.add(receiver_account)
        notification.save()

@receiver(post_save, sender=Account)
def generate_account_qr_code(sender, instance, created, **kwargs):
    if created:  
        account_data = {
            "username": instance.user.username,
            "email": instance.user.email,
            "bio": instance.bio,
        }

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(account_data))
        qr.make(fit=True)

        # Convert the QR code to an image
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the QR code to the `qr_code` field
        instance.qr_code.save(f"{instance.user.username}_qr.png", ContentFile(buffer.read()), save=False)
        buffer.close()
        instance.save()

