from __future__ import annotations
import os
import re
from pydoc import locate
from syenv.exceptions import SysenvError
from typing import Any, Dict, Generator, List


class Syenv:
    """The Syenv class definition.
    Load the environment variables which contains the prefix (if needed)
    and auto hydrate itself with the variables retrieved.

    Attributes:
        as_dict (Dict[str, Any]): The imported variables as dict format.
    """

    _INTERP_REGEX: str = r'{{(\w+)}}'
    _DEFAULT_TYPE_SEP: str = '::'
    _DEFAULT_KEEP_PREFIX: bool = False
    _SKIPED_ATTR: List[str] = ['_prefix', '_type_separator', '_keep_prefix']

    def __init__(
        self,
        prefix: str = '',
        *,
        type_separator: str = _DEFAULT_TYPE_SEP,
        keep_prefix: bool = _DEFAULT_KEEP_PREFIX,
    ) -> None:
        """The Syenv class constructor.
        Hydrate the object with the variables retrieved.

        Args:
            prefix (str, optional): The variables prefixe.
                Default to Syenv._DEFAULT_TYPE_SEP.
            type_separator (str, optional): The pattern that seperate the
                type from the value. Default to Syenv._DEFAULT_TYPE_SEP.
            keep_prefix (bool, optional): Indicate if Syenv should keep this
                prefix for its attributes name.
                Default to Syenv._DEFAULT_KEEP_PREFIX.
        """

        self._prefix: str = prefix
        self._type_separator: str = type_separator
        self._keep_prefix: bool = keep_prefix
        self._loadenv()

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Return all mutated variables in dict format.

        Returns:
            Dict[str, Any]: The formated variables.
        """

        return {k: v for k, v in self.__iter__()}

    def from_pattern(self, pattern: str) -> Dict[str, Any]:
        """Get the variables which names matches with the pattern
        passed in parameter.

        Args:
            pattern (str): The string to search in attributes.

        Returns:
            Dict[str, Ant]: The attributes matched.
        """

        return {k: v for k, v in self.as_dict.items() if re.search(pattern, k)}

    def _loadenv(self) -> None:
        """Hydrate the Syenv object with the environment variables
        retrieved.

        Notes:
            The prefix of all environment variables
            is suppressed during the mutation.
        """

        for env_key in os.environ.keys():
            if re.match(r'^%s' % self._prefix, env_key):
                setattr(
                    self,
                    env_key
                    if self._keep_prefix
                    else self._sub_prefix(env_key),
                    self._interpolate(os.environ[env_key]),
                )

    def _interpolate(self, val: str) -> str:
        """Trying to replace an interpolated variable string with
        the correct values.

        Exemples:
            We are considering 2 environments variables that are:
                MY_GENERIC_VAR=hello
                MY_SPECIFIC_VAR={{MY_GENERIC_VAR}} world!

            self._interpolate(os.environ['MY_SPECIFIC_VAR'])
            >>> 'hello world!'

        Args:
            val (str): The variable value that may contains
                some interpolations.

        Raises:
            SysenvError: If the interpolated variable doesn't exists.

        Returns:
            str: The formated variable value.
        """

        if keys := re.findall(self._INTERP_REGEX, val):
            for key in keys:
                try:
                    val = val.replace(
                        '{{%s}}' % key,
                        str(
                            getattr(
                                self,
                                key
                                if self._keep_prefix
                                else self._sub_prefix(key),
                            )
                        ),
                    )
                except AttributeError:
                    raise SysenvError(
                        f'The interpolated key "{key}" doesn\'t '
                        f'exists in environment variables, '
                        f'or it is called before assignement.'
                    )

        return self._parse(val)

    def _parse(self, val: str) -> Any:
        """Trying to parse a variable value to the correct
        type specified to the variable value. If no type are
        specified, the str type is used by default.

        Exemples:
            self._parse('int:22')
            >>> 22

            self._parse('some_string')
            >>> 'some_string'

            self._parse('pathlib.Path:statics/js')
            >>> PosixPath('statics/js')

            self._parse('dateutil.parser.parse:2000-01-01')
            >>> datetime.datetime(2000, 01, 01, 0, 0)

        Notes:
            The parsing string format is compatible with
            the interpolation process.

            Thus, considering the following environment variables:
                STATICS_PATH=pathlib.Path:statics
                JS_FILES_PATH=pathlib.Path:{{STATICS_PATH}}/js

            We can easily parse the JS_FILES_PATH variable as follow:
                self._pase(os.environ['JS_FILES_PATH'])
                >>> PosixPath('statics/js')

        Args:
            val (str): The environment variable value.

        Raises:
            SysenvError: If the type specified dosen't exists
                or if the variable value passed in the type parameter
                doesn't match with its requirements.

        Returns:
            Any: The parsed value in the correct type.
        """

        env_parts: List[str] = val.split(self._type_separator)
        env_type, env_val = (
            env_parts if len(env_parts) == 2 else ['str', env_parts[0]]
        )

        try:
            return locate(env_type)(env_val)
        except TypeError:
            raise SysenvError(
                f'The type "{env_type}" doesn\'t exists, or the argument '
                f'"{env_val}" doesn\'t matching with the '
                f'{env_type} parameters.'
            )

    def _sub_prefix(self, key: str) -> str:
        """Suppress prefix in the key.

        Args:
            key (str): The key to process.

        Returns:
            str: The cleaned key.
        """

        return key.replace(self._prefix, '')

    def __iter__(self) -> Generator:
        """Overload the __iter__ method for suppress useless attributes."""

        for key, val in self.__dict__.items():
            if key not in self._SKIPED_ATTR:
                yield key, val