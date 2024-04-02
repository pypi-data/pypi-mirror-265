from .core import ManageOTP

class TwoFa:

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.required_kwargs = ["issuer_name", "storage"]
    

    def generate_qr_code(self, **kwargs) -> dict:
        """
        :identifier Identifier is the key use to identify the rightful own of the OTP
        """

        required_kwargs = ["storage", "identifier"]

        # Validate to be sure that the require fields is pass to the kwargs data
        for req_kwarg in required_kwargs:
            if req_kwarg not in [i for i in kwargs.keys()]:
                return TwoFa.build_body(status=False, message=f"{req_kwarg} is required")
        

        # Check to be sure storage type is not empty
        if kwargs.get("storage") == "":
            return TwoFa.build_body(status=False, message="Kindly enter the correct storage type")
        
        # Validate the storage type
        if kwargs.get("storage") != "cloudinary" and kwargs.get("storage") != "s3bucket":
            return TwoFa.build_body(status=False, message="storage can either be 'cloudinary or s3bucket' ")
        

        # Make use of cloudinary as the storage for QRCode image
        if kwargs.get("storage") == "cloudinary":
            required_cloudinary_key = ["cloud_name", "api_key", "api_secret"]
            for key in required_cloudinary_key:
                if key not in [i for i in kwargs.keys()]:
                    return TwoFa.build_body(status=False, message=f"{key} is required as part of cloudinary configuration")
                
        
        if kwargs.get("storage") == "s3bucket":
            required_s3_key = ["bucket_name", "access_key", "secret_access"]
            for key in required_s3_key:
                if key not in [i for i in kwargs.keys()]:
                    return TwoFa.build_body(status=False, message=f"{key} is required as part of s3 bucket configuration")

        user_key, url = ManageOTP.create_otp(
                storage=kwargs.get("storage"),
                config=kwargs,
                identifier=kwargs.get("identifier"),
                issuer_name=self.kwargs.get("issuer_name")
            )
        if not user_key:
            return TwoFa.build_body(status=False, message=url)
        
        return TwoFa.build_body(status=True, url=url, user_key=user_key, identifier=kwargs.get("identifier"))

    def validate_code(self, user_key: str, code: str) -> bool:
        check = ManageOTP.verify_otp(user_key, code)
        if check:
            return TwoFa.build_body(status=True, message="valid")
        else:
            return TwoFa.build_body(status=False, message="not valid")


    @staticmethod
    def build_body(**kwargs) -> dict:
        return dict(kwargs)
