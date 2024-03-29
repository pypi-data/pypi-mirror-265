import inflection

from komodo.framework.komodo_user import KomodoUser
from komodo.store.user_store import UserStore


class UserLoader:
    @classmethod
    def load(cls, email) -> [KomodoUser, None]:
        user = cls.load_appliance_user(email) or cls.load_system_user(email)
        return user

    @classmethod
    def load_appliance_user(cls, email) -> [KomodoUser, None]:
        try:
            user = UserStore().retrieve_user(email)
            return KomodoUser(name=user.name, email=user.email) if user else None
        except Exception as e:
            print("Error while loading user: ", e)
            return None

    @classmethod
    def load_system_user(cls, email) -> [KomodoUser, None]:
        domain = email.split('@')[1].split('.')
        if 'kmdo' in domain or 'komodoapp' in domain:
            name = inflection.titleize(email.split('@')[0])
            return KomodoUser(name=name, email=email)
        return None

    @classmethod
    def is_power_user(cls, email) -> bool:
        return email == "ryan@kmdo.app"
