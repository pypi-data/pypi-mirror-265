import os
from pyqrcode import QRCode

import string, random
import qrcode
import pyotp
import boto3
import uuid
from PIL import Image
import io

import cloudinary
import cloudinary.uploader
import cloudinary.api


class ManageOTP:
    
    @staticmethod
    def image_name():
        res = ''.join(random.choices(string.digits, k=4))
        code = str(res)
        _id = "image{}".format(code)
        return _id
    
    @staticmethod
    def create_otp(**kwargs):
        # def create_otp(cloud_name: str, api_key: str, api_secret: str, identifier: str, issuer_name:str):
        try:
            if kwargs.get("storage") == "cloudinary":
                cloudinary.config(cloud_name=kwargs.get("config").get("cloud_name"), api_key=kwargs.get("config").get("api_key"), api_secret=kwargs.get("config").get("api_secret"))
                user_keys = pyotp.random_base32()
                otp = pyotp.totp.TOTP(user_keys).provisioning_uri(kwargs.get("identifier"), issuer_name=kwargs.get("issuer_name"))
                img = qrcode.make(otp)
                img_url = cloudinary.uploader.upload(ManageOTP.image_to_byte_array(img))
                return user_keys, img_url.get("url")
            
            if kwargs.get("storage") == "s3bucket":
                s3_client = boto3.client('s3', aws_access_key_id=kwargs.get("config").get("access_key"), aws_secret_access_key=kwargs.get("config").get("secret_access"))

                user_keys = pyotp.random_base32()
                otp = pyotp.totp.TOTP(user_keys).provisioning_uri(kwargs.get("identifier"), issuer_name=kwargs.get("issuer_name"))
                img = qrcode.make(otp)
                file_name = f"{uuid.uuid4()}.png"
                s3_client.put_object(Bucket=kwargs.get("config").get("bucket_name"), Body=ManageOTP.image_to_byte_array(img), Key=file_name)
                img_url = f"https://{kwargs.get('config').get('bucket_name')}.s3.amazonaws.com/{file_name}"

                return user_keys, img_url
        except Exception as e:
            return False, e
    
    @staticmethod
    def verify_otp(identifier: str, otp_code: str):
        totp = pyotp.TOTP(identifier)
        if totp.now() == otp_code:
            return True
        return False
    
    
    def create_time_base_otp(self):
        data = QRCode.objects.filter(email=self.email).first()
        
        totp = pyotp.TOTP(data.user_key, interval=600)
        otpcode = totp.now()
        # print(otpcode)
        self.send.send_otp(self.email, otpcode)
        pass
    
    def verify_time_base_otp(self):
        data = QRCode.objects.filter(email=self.email).first()
        totp = pyotp.TOTP(data.user_key, interval=600)
        check = totp.verify(self.otp_code)
        return check
    
    @staticmethod
    def image_to_byte_array(image: Image) -> bytes:
        # BytesIO is a file-like buffer stored in memory
        imgByteArr = io.BytesIO()
        # image.save expects a file-like as a argument
        image.save(imgByteArr, format=image.format)
        # Turn the BytesIO object back into a bytes object
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr
    
    @staticmethod
    def image_name():
        res = ''.join(random.choices(string.digits, k=4))
        code = str(res)
        _id = "image{}".format(code)
        return _id