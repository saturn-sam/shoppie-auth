from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    # Add custom claims
    refresh['is_staff'] = user.is_staff
    # refresh['username'] = user.username  # optional

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
