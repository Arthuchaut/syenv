from pathlib import Path
from pydoc import locate
from typing import Any, Dict
import pytest
from syenv import Syenv
from syenv.exceptions import SysenvError


class TestSensy:
    def test__loadenv(
        self,
        patched_syenv: Syenv,
        expected_env: Dict[str, Any],
    ) -> None:
        patched_syenv._loadenv()

        for key, val in expected_env.items():
            assert getattr(patched_syenv, key) == val

    def test__interpolate(
        self,
        patched_syenv: Syenv,
    ) -> None:
        patched_syenv.INTERP_GENERIC = Path('tests')
        result: Any = patched_syenv._interpolate(
            'pathlib.Path::{{SYENV_TEST_INTERP_GENERIC}}/.env'
        )
        expected: Path = Path('tests/.env')

        assert result == expected

        with pytest.raises(SysenvError):
            patched_syenv._interpolate(
                'pathlib.Path::{{SYENV_TEST_UNKNOWN_VARIABLE}}/.env'
            )

    def test__parse(
        self,
        patched_syenv: Syenv,
        expected_env_unparsed: Dict[str, str],
    ) -> None:
        for exp_val in expected_env_unparsed.values():
            result: Any = patched_syenv._parse(exp_val)
            exp_type: type = locate(exp_val.split(':')[0])
            assert isinstance(result, exp_type)

        with pytest.raises(SysenvError):
            patched_syenv._parse('unknown_type::some value')

    def test__sub_prefix(self, patched_syenv: Syenv, prefix: str) -> None:
        key: str = f'{prefix}MY_KEY'
        expected: str = 'MY_KEY'

        assert patched_syenv._sub_prefix(key) == expected

    def test___iter__(self, patched_syenv: Syenv) -> None:
        setattr(patched_syenv, 'SOME_VAR', None)
        setattr(patched_syenv, 'ANOTHER_VAR', None)

        assert len([_ for _ in patched_syenv.__iter__()]) == 2

    def test_as_dict(
        self,
        prefix: str,
        expected_env: Dict[str, Any],
    ) -> None:
        env: Syenv = Syenv(prefix)
        assert env.as_dict == expected_env
