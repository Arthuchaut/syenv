from typing import Any, Dict
from sysenv import Sysenv


class TestSensy:
    def test_env_loading(
        self, prefix: str, expected_env: Dict[str, Any]
    ) -> None:
        env: Sysenv = Sysenv(prefix)

        for key, val in env.__iter__():
            assert val == expected_env[key]
            assert type(val) == type(expected_env[key])