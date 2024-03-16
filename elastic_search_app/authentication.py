from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class OctoxlabsJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        # Ensure the token is valid and has a username field
        try:
            user = self.get_user(validated_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed('User not found or token is invalid.')

        if not user or not user.is_active:
            raise exceptions.AuthenticationFailed('User not found or inactive.')

        return (user, validated_token)
