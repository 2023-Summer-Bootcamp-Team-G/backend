from django.conf import settings
from django.core.signing import Signer, BadSignature

bypass = True  # True
signer = Signer(settings.SECRET_KEY)


def encrypt_resource_id(resource_id):
    if bypass:
        return resource_id
    else:
        signed_resource_id = signer.sign(str(resource_id))
        return signed_resource_id


def decrypt_resource_id(signed_resource_id):
    if bypass:
        return signed_resource_id
    else:
        try:
            original_resource_id = signer.unsign(str(signed_resource_id))
            return original_resource_id
        except BadSignature:
            return None
