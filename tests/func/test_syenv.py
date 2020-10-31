from typing import Any, Dict
from syenv import Syenv


class TestSensy:
    def test_env_loading(
        self, prefix: str, expected_env: Dict[str, Any]
    ) -> None:
        env: Syenv = Syenv(prefix)

        for key, val in env.__iter__():
            assert val == expected_env[key]
            assert type(val) == type(expected_env[key])