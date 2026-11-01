import qrcode
from io import BytesIO
import base64
import uuid
def generateCode(text: str, img_name: str = f'QRcode{uuid.uuid2}.png') ->:
    code = qrcode.QRcode(
        version =1 , box_size=10, border=4
    )
    code.add_data(text)
    code.make(fit=True)
    img = code.make(fill_color='black',back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    qrCode = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
    return qrCode  
