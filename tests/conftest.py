from pathlib import Path
from pydoc import locate
from _pytest.monkeypatch import MonkeyPatch
from syenv.syenv import Syenv
from typing import Any, Callable, Dict, List
import pytest
import dotenv

FAKE_ENV_FILE: Path = Path('tests/.env')
FAKE_EXPECTED_ENV_FILE: Path = Path('tests/.env-expected')
dotenv.load_dotenv(FAKE_ENV_FILE)


@pytest.fixture
def prefix() -> str:
    return 'SYENV_TEST_'


@pytest.fixture
def patched_syenv(
    monkeypatch: MonkeyPatch, prefix: str
) -> Callable[[bool], Syenv]:
    def handler(keep_prefix: bool = False) -> Syenv:
        monkeypatch.setattr(Syenv, '__init__', lambda self: None)
        env: Syenv = Syenv()
        env._prefix = prefix
        env._type_separator = '::'
        env._keep_prefix = keep_prefix
        return env

    return handler


@pytest.fixture
def expected_env_unparsed(prefix: str) -> Dict[str, Any]:
    def handler(keep_prefix: bool = False) -> Dict[str, Any]:
        expected: Dict[str, Any] = {}

        for line in FAKE_EXPECTED_ENV_FILE.read_text(encoding='utf-8').split(
            '\n'
        ):
            if line:
                line = line.split('=')
                expected[
                    line[0] if keep_prefix else line[0].replace(prefix, '')
                ] = line[1]

        return expected

    return handler


@pytest.fixture
def expected_env(prefix: str) -> Dict[str, Any]:
    def handler(keep_prefix: bool = False) -> Dict[str, Any]:
        expected: Dict[str, Any] = {}

        for line in FAKE_EXPECTED_ENV_FILE.read_text(encoding='utf-8').split(
            '\n'
        ):
            if line:
                line = line.split('=')
                val_parts: List[str] = line[1].split('::')
                expected[
                    line[0] if keep_prefix else line[0].replace(prefix, '')
                ] = locate(val_parts[0])(val_parts[1])

        return expected

    return handler