""" Handler for tokens """
import datetime as dt
import jwt

from django.conf import settings

from user.models import Auth, User


class TokenHandler:
    def get_payload(self, request):

        # pylint: disable=no-self-use
        header = request.headers.get("Authorization", None)
        if (not header or len(header.split(" ")) != 2 or
                header.split(" ")[0].lower() != "bearer"):
            return None, None

        try:
            token = jwt.decode(header.split(
                " ")[1], settings.SECRET_KEY, algorithms='HS256')
        except jwt.InvalidTokenError:
            return None, None

        expiration_date = dt.datetime.strptime(token['expiration_date'],
                                               '%Y-%m-%d %H:%M:%S.%f')

        db_token = Auth.objects.filter(token=header.split(" ")[1]).first()

        if (expiration_date < dt.datetime.now() or not db_token or
                db_token.is_disabled):
            return None, None

        user = User.objects.filter(
            email=token["email"], is_active=True).first()

        if not user:
            return None, None

        return token, user

    def is_owner(self, token_email, request_child):

        # pylint: disable=no-self-use
        return token_email == request_child

    def has_permissions(self, profiles, user):
        return user.profile.filter(names__in=profiles).exists()
