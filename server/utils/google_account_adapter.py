from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class GoogleAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email
        return user
