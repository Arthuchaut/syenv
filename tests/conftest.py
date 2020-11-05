from pathlib import Path
from pydoc import locate
from typing import Any, Dict, List
import pytest
import dotenv

FAKE_ENV_FILE: Path = Path('tests/.env')
FAKE_EXPECTED_ENV_FILE: Path = Path('tests/.env-expected')
dotenv.load_dotenv(FAKE_ENV_FILE)


@pytest.fixture
def prefix() -> str:
    return 'SYENV_TEST_'


@pytest.fixture
def expected_env_unparsed(prefix: str) -> Dict[str, Any]:
    expected: Dict[str, Any] = {}

    for line in FAKE_EXPECTED_ENV_FILE.read_text(encoding='utf-8').split('\n'):
        if line:
            line = line.split('=')
            expected[line[0].replace(prefix, '')] = line[1]

    return expected


@pytest.fixture
def expected_env(prefix: str) -> Dict[str, Any]:
    expected: Dict[str, Any] = {}

    for line in FAKE_EXPECTED_ENV_FILE.read_text(encoding='utf-8').split('\n'):
        if line:
            line = line.split('=')
            val_parts: List[str] = line[1].split('::')
            expected[line[0].replace(prefix, '')] = locate(val_parts[0])(
                val_parts[1]
            )

    return expected