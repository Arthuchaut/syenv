from pathlib import Path
from pydoc import locate
from typing import Any, Callable, Dict
import pytest
from syenv import Syenv
from syenv.exceptions import SysenvError


class TestSensy:
    def test__loadenv(
        self,
        patched_syenv: Callable[[bool], Syenv],
        expected_env: Callable[[bool], Dict[str, Any]],
    ) -> None:
        env: Syenv = patched_syenv()
        env_with_prefix: Syenv = patched_syenv(keep_prefix=True)
        env._loadenv()
        env_with_prefix._loadenv()

        for key, val in expected_env().items():
            assert getattr(env, key) == val

        for key, val in expected_env(keep_prefix=True).items():
            assert getattr(env_with_prefix, key) == val

    def test__interpolate(
        self,
        patched_syenv: Callable[[bool], Syenv],
    ) -> None:
        env: Syenv = patched_syenv()
        env.INTERP_GENERIC = Path('tests')
        result: Any = env._interpolate(
            'pathlib.Path%s{{SYENV_TEST_INTERP_GENERIC}}/.env'
            % env._DEFAULT_TYPE_SEP
        )
        expected: Path = Path('tests/.env')

        assert result == expected

        with pytest.raises(SysenvError):
            env._interpolate(
                'pathlib.Path%s{{SYENV_TEST_UNKNOWN_VARIABLE}}/.env'
                % env._DEFAULT_TYPE_SEP
            )

    def test__parse(
        self,
        patched_syenv: Callable[[bool], Syenv],
        expected_env_unparsed: Callable[[bool], Dict[str, Any]],
    ) -> None:
        env: Syenv = patched_syenv()

        for exp_val in expected_env_unparsed().values():
            result: Any = env._parse(exp_val)
            exp_type: type = locate(exp_val.split(':')[0])
            assert isinstance(result, exp_type)

        with pytest.raises(SysenvError):
            env._parse(f'unknown_type{env._DEFAULT_TYPE_SEP}some value')

    def test__sub_prefix(
        self, patched_syenv: Callable[[bool], Syenv], prefix: str
    ) -> None:
        env: Syenv = patched_syenv()
        key: str = f'{prefix}MY_KEY'
        expected: str = 'MY_KEY'

        assert env._sub_prefix(key) == expected

    def test___iter__(self, patched_syenv: Callable[[bool], Syenv]) -> None:
        env: Syenv = patched_syenv()

        setattr(env, 'SOME_VAR', None)
        setattr(env, 'ANOTHER_VAR', None)

        assert len([_ for _ in env.__iter__()]) == 2

    def test_as_dict(
        self,
        prefix: str,
        expected_env: Callable[[bool], Dict[str, Any]],
    ) -> None:
        env: Syenv = Syenv(prefix)
        assert env.as_dict == expected_env()

    def test_from_pattern(self, prefix: str) -> None:
        env: Syenv = Syenv(prefix, keep_prefix=True)
        expected: Dict[str, str] = {
            'SYENV_TEST_MULTI_INTERP_GEN': 'this',
            'SYENV_TEST_MULTI_INTERP_SPE_1': 'this is',
            'SYENV_TEST_MULTI_INTERP_SPE_2': 'my',
            'SYENV_TEST_MULTI_INTERP_SPE_3': 'this is my test!',
        }

        assert env.from_pattern('MULTI_INTERP_', keep_pattern=True) == expected