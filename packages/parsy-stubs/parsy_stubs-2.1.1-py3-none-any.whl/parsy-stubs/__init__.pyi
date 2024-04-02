from __future__ import annotations

import enum
from dataclasses import dataclass
from re import Pattern
from typing import (
    Any,
    Callable,
    FrozenSet,
    Generator,
    Generic,
    Sequence,
    TypeVar,
    overload,
)

Input = TypeVar("Input", bound=Sequence)
Output = TypeVar("Output")

T = TypeVar("T")

def noop(x: T) -> T: ...
def line_info_at(stream: Input, index: int) -> tuple[int, int]: ...

class ParseError(RuntimeError, Generic[Input]):
    def __init__(self, expected: FrozenSet[str], stream: Input, index: int): ...
    def line_info(self) -> str: ...
    def __str__(self) -> str: ...

@dataclass
class Result(Generic[Output]):
    status: bool
    index: int
    value: Output
    furthest: int
    expected: FrozenSet[str]

    @staticmethod
    def success(index: int, value: Output) -> Result[Output]: ...
    @staticmethod
    def failure(index: int, expected: FrozenSet[str]) -> Result: ...
    def aggregate(self, other: Result) -> Result[Output]: ...

class Parser(Generic[Input, Output]):
    """
    A Parser is an object that wraps a function whose arguments are
    a string to be parsed and the index on which to begin parsing.
    The function should return either Result.success(next_index, value),
    where the next index is where to continue the parse and the value is
    the yielded value, or Result.failure(index, expected), where expected
    is a string indicating what was expected, and the index is the index
    of the failure.
    """

    def __init__(
        self,
        wrapped_fn: Callable[[Input, int], Result[Output]],
    ): ...
    def __call__(
        self,
        stream: Input,
        index: int,
    ) -> Result[Output]: ...
    def parse(
        self,
        stream: Input,
    ) -> Output: ...
    def parse_partial(
        self,
        stream: Input,
    ) -> tuple[Output, Input]: ...
    def bind(
        self,
        bind_fn: Callable[[Output], Parser[Input, T]],
    ) -> Parser[Input, T]: ...
    def map(
        self,
        map_function: Callable[[Output], T],
    ) -> Parser[Input, T]: ...
    def combine(self, combine_fn: Callable[..., T]) -> Parser[Input, T]: ...
    def combine_dict(self, combine_fn: Callable[..., T]) -> Parser[Input, T]: ...
    def concat(self) -> Parser[Input, str]: ...
    def then(
        self,
        other: Parser[Input, T],
    ) -> Parser[Input, T]: ...
    def skip(
        self,
        other: Parser,
    ) -> Parser[Input, Output]: ...
    def result(
        self,
        value: T,
    ) -> Parser[Input, T]: ...
    def many(self) -> Parser[Input, list[Output]]: ...
    def times(
        self, min: int, max: int | None = None
    ) -> Parser[Input, list[Output]]: ...
    def at_most(
        self,
        n: int,
    ) -> Parser[Input, list[Output]]: ...
    def at_least(
        self,
        n: int,
    ) -> Parser[Input, list[Output]]: ...
    @overload
    def optional(
        self,
        default: None = None,
    ) -> Parser[Input, Output | None]: ...
    @overload
    def optional(
        self,
        default: T,
    ) -> Parser[Input, Output | T]: ...
    def until(
        self,
        other: Parser,
        *,
        min: int = ...,
        max: int = ...,
        consume_other: bool = ...,
    ) -> Parser[Input, list[Output]]: ...
    def sep_by(
        self,
        sep: Parser,
        min: int = ...,
        max: int = ...,
    ) -> Parser[Input, list[Output]]: ...
    def desc(
        self,
        description: str,
    ) -> Parser[Input, Output]: ...
    def mark(
        self,
    ) -> Parser[Input, tuple[tuple[int, int], Output, tuple[int, int]]]: ...
    def tag(
        self,
        name: str,
    ) -> Parser[Input, tuple[str, Output]]: ...
    def should_fail(
        self,
        description: str = ...,
    ) -> Parser[Input, Output]: ...
    def __add__(
        self,
        other: Parser,
    ) -> Parser[Input, Output]: ...
    def __mul__(
        self,
        other: Parser,
    ) -> Parser[Input, list[Output]]: ...
    def __or__(
        self,
        other: Parser[Input, T],
    ) -> Parser[Input, Output | T]: ...
    def __rshift__(
        self,
        other: Parser[Input, T],
    ) -> Parser[Input, T]: ...
    def __lshift__(
        self,
        other: Parser,
    ) -> Parser[Input, Output]: ...

def alt(*parsers: Parser) -> Parser: ...
def seq(
    *parsers: Parser[Input, Any],
    **kw_parsers: Parser[Input, Any],
) -> Parser[Input, tuple]: ...

P = TypeVar("P", bound=Parser)
ParseGen = Generator[Parser[Input, Any] | Any, Any, T]

@overload
def generate(gen: Callable[[], ParseGen[Input, T]]) -> Parser[Input, T]: ...
@overload
def generate(
    gen: str,
) -> Callable[[Callable[[], ParseGen[Input, T]]], Parser[Input, T]]: ...

index: Parser[str, int]
line_info: Parser[str, tuple[int, int]]

def success(value: T) -> Parser[Input, T]: ...
def fail(expected: str) -> Parser: ...
def string(
    expected_string: str,
    transform: Callable[[str], str] = ...,
) -> Parser[str, str]: ...
def regex(
    exp: str | Pattern[str],
    flags: int = ...,
    group: int | str | tuple = ...,
) -> Parser[str, str]: ...

StrOrBytes = TypeVar("StrOrBytes", str, bytes)

def test_item(
    func: Callable[[T], bool], description: str
) -> Parser[Sequence[T], T]: ...
def test_char(
    func: Callable[[StrOrBytes], bool], description: str
) -> Parser[StrOrBytes, StrOrBytes]: ...
def match_item(
    item: T,
    description: str | None = ...,
) -> Parser[Sequence[T], T]: ...
def string_from(
    *strings: str,
    transform: Callable[[str], str] = ...,
) -> Parser[str, str]: ...
def char_from(string: StrOrBytes) -> Parser[StrOrBytes, StrOrBytes]: ...
def peek(parser: Parser[Input, T]) -> Parser[Input, T]: ...

any_char: Parser[str, str]

whitespace: Parser[str, str]

letter: Parser[str, str]

digit: Parser[str, str]
decimal_digit: Parser[str, str]
eof: Parser[str, None]

E = TypeVar("E", bound=enum.Enum)

def from_enum(enum_cls: type[E], transform=noop) -> Parser[str, E]: ...
