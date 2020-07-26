from fake_useragent import UserAgent
from faker import Faker
from sqlalchemy.orm import sessionmaker

from .variable_manager import VariableManager


class GlobalVariable(VariableManager):
    def __init__(self):
        super().__init__(load_file=True)
        self._db = None
        self._user_agent = None
        self._faker = None
        self._title_service = None

        # self.init_ua()
        self.init_faker()

        if self.get_conf("SERVER_NAME") is None:
            self.set_conf("SERVER_NAME", "v2ray_subscribe")

    def init_faker(self):
        self._faker = Faker()

    def init_ua(self):
        self._user_agent = UserAgent(verify_ssl=False, use_cache_server=False)

    def init_db(self, engine):
        if self.get_conf_bool("ENABLE_DATABASE", default=True):
            self._db = sessionmaker(bind=engine)

    def get_db(self):
        return self._db()

    def get_user_agent(self):
        return self._faker.user_agent()

    # def get_title(self):
    #     return self._title_service.get()
