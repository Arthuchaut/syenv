from typing import Any, Callable, Dict
from syenv import Syenv


class TestSensy:
    def test_env_loading(
        self, prefix: str, expected_env: Callable[[bool], Dict[str, Any]]
    ) -> None:
        env: Syenv = Syenv(prefix)

        for key, val in env.__iter__():
            assert val == expected_env()[key]
            assert type(val) == type(expected_env()[key])