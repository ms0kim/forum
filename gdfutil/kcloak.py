from django.conf import settings
from keycloak import KeycloakAdmin, KeycloakOpenID


class KeyOpenID:
    def __init__(self):
        self.url = settings.KEYCLOAK_BASE_URL
        self.client_id = settings.KEYCLOAK_WEB_CLIENT_ID
        self.realm_name = settings.KEYCLOAK_REALM_NAME
        self.client_secret = settings.KEYCLOAK_WEB_CLIENT_SECRET

        self.OpenIdController = KeycloakOpenID(
            server_url=self.url,
            client_id=self.client_id,
            realm_name=self.realm_name,
            client_secret_key=self.client_secret,
        )

        self.public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            + self.OpenIdController.public_key()
            + "\n-----END PUBLIC KEY-----"
        )

        self.kcid = ""


class KeyAdmin(KeyOpenID):
    def __init__(self):
        super().__init__()
        self.admin_secret = settings.KEYCLOAK_ADMIN_SECRET
        self.admin_name = settings.KEYCLOAK_ADMIN_NAME
        self.admin_pw = settings.KEYCLOAK_ADMIN_PASSWORD

        self.AdminController = KeycloakAdmin(
            server_url=self.url,
            client_secret_key=self.admin_secret,
            user_realm_name=self.realm_name,
            username=self.admin_name,
            password=self.admin_pw,
            verify=True,
        )

keyOpen = KeyOpenID()
oc = keyOpen.OpenIdController
keyAdmin = KeyAdmin()
ac = keyAdmin.AdminController


def verify_token(access_token: str, sig: bool=True, aud: bool=True, exp: bool=True) -> tuple:
    if access_token[:6] == "Bearer":
        access_token = access_token[7:]

    try:
        options = {"verify_signature": sig, "verify_aud": aud, "verify_exp": exp}
        token_info = oc.decode_token(
            access_token, key=keyOpen.public_key, options=options
        )
        return True, token_info
    except Exception as e:
        return False, e
    
def userInfoByToken(token: str, verify: bool = False) -> dict | None:
    if verify :
        if not verify_token(token) :
            return None
            
    if token.startswith("Bearer"):
        _, token = token.split(" ")
    return oc.userinfo(token)
  