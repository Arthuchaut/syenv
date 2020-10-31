from pathlib import Path
from pydoc import locate
from typing import Any, Dict
import pytest
from _pytest.monkeypatch import MonkeyPatch, monkeypatch
from sysenv import Sysenv
from sysenv.exceptions import SysenvError


class TestSensy:
    def test__loadenv(
        self,
        prefix: str,
        expected_env: Dict[str, Any],
        monkeypatch: MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(Sysenv, '__init__', lambda self: None)
        env: Sysenv = Sysenv()
        env._prefix = prefix
        env._loadenv()

        for key, val in expected_env.items():
            assert getattr(env, key) == val

    def test__interpolate(
        self,
        prefix: str,
        monkeypatch: MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(Sysenv, '__init__', lambda self: None)
        env: Sysenv = Sysenv()
        env._prefix = prefix
        env.INTERP_GENERIC = Path('tests')
        result: Any = env._interpolate(
            'pathlib.Path:{{SYSENV_TEST_INTERP_GENERIC}}/.env'
        )
        expected: Path = Path('tests/.env')

        assert result == expected

        with pytest.raises(SysenvError):
            env._interpolate(
                'pathlib.Path:{{SYSENV_TEST_UNKNOWN_VARIABLE}}/.env'
            )

    def test__parse(
        self,
        prefix: str,
        expected_env_unparsed: Dict[str, str],
        monkeypatch: MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(Sysenv, '__init__', lambda self: None)
        env: Sysenv = Sysenv()
        env._prefix = prefix

        for exp_val in expected_env_unparsed.values():
            result: Any = env._parse(exp_val)
            exp_type: type = locate(exp_val.split(':')[0])
            assert isinstance(result, exp_type)

        with pytest.raises(SysenvError):
            env._parse('unknown_type:some value')

    def test__sub_prefix(self, prefix: str, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(Sysenv, '__init__', lambda self: None)
        env: Sysenv = Sysenv()
        env._prefix = prefix
        key: str = f'{prefix}MY_KEY'
        expected: str = 'MY_KEY'

        assert env._sub_prefix(key) == expected

    def test___iter__(self, prefix: str, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(Sysenv, '__init__', lambda self: None)
        env: Sysenv = Sysenv()
        env._prefix = prefix

        setattr(env, 'SOME_VAR', None)
        setattr(env, 'ANOTHER_VAR', None)

        assert len([_ for _ in env.__iter__()]) == 2

    def test_as_dict(
        self,
        prefix: str,
        expected_env: Dict[str, Any],
        monkeypatch: MonkeyPatch,
    ) -> None:
        env: Sysenv = Sysenv(prefix)
        assert env.as_dict == expected_env