from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth as firebase_auth

from users.models import User


class FirebaseAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            decoded_token = firebase_auth.verify_id_token(token)

            uid = decoded_token["uid"]
            email = decoded_token.get("email", "")

            user, created = User.objects.get_or_create(
                firebase_uid=uid,
                defaults={
                    "email": email,
                    "role": "buyer"
                }
            )

            return (user, None)

        except Exception:
            raise AuthenticationFailed("Invalid or expired Firebase token")