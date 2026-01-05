import qrcode
import base64
from io import BytesIO
from datetime import datetime, timedelta

def generate_qr(user_id):
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    expires_str = expires_at.strftime('%Y-%m-%d %H:%M:%S')

    site_url = "http://192.168.1.156:5000"

    qr = qrcode.make(site_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")

    base64_img = f"data:image/png;base64,{base64_img}"

    return base64_img, expires_str
