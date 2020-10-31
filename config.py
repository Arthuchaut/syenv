from typing import Any, Dict, overload
import sysenv
import dotenv
from datetime import datetime
from pprint import pp

dotenv.load_dotenv('tests/.env')


class Config(sysenv.Sysenv):
    def __init__(self, prefix: str) -> None:
        super().__init__(prefix)
        self.another_var: str = 'Hey!'

    @property
    def ftp_uri(self) -> datetime:
        return f'{self.STR_VAR}:{self.INT_VAR}'


conf: Config = Config('SYSENV_TEST_')

pp(conf.as_dict)
print(conf.ftp_uri)


# class Config(sysenv.Sysenv):
#     cur_date: datetime = datetime.now()
#     # @property
#     # def current_date(self) -> datetime:
#     #     return datetime.now()

#     @property
#     def as_dict(self) -> Dict[str, Any]:
#         return {**super().as_dict, **{k: v for k, v in self.__iter__()}}


# conf: Config = Config('SYSENV_TEST_')

# pp(conf.as_dict)
