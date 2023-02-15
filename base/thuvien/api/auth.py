from ..models import NguoiMuon

def createToken(max_length=100):
        import random
        import string
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(max_length))


def auth(token):
    try:
        user = NguoiMuon.objects.get(token=token)
        return user
    except:
        return None