import qrcode
import json
from io import BytesIO
from django.core.mail import send_mail

def send_mail_for_user(subject , message , recipient_list , from_email , fail_silently) :
    subject = "testing utlis" 
    message = "testing send mail fuction"
    send_mail(subject , message , recipient_list, from_email , fail_silently=False)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
