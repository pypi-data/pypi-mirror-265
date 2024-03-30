"""Parser and generator for a tag: scheme URI."""

from __future__ import annotations

import datetime
import importlib.resources
from dataclasses import dataclass
from datetime import UTC
from functools import cache, total_ordering
from typing import ClassVar, Protocol, TypedDict, runtime_checkable

import lark


@dataclass(frozen=True, order=True, slots=True)
class TagURI:
    """A representation of data from parsed Tag URI.

    The tagging_entity is a TaggingEntity instance having the domain or email of the
    authority section of the tag, and the date.

    The specific is a path-like identifier for the URI.

    The fragment is an optional sub-identifier specified by the # at the end of the URI.

    >>> tag_uri = TagURI.parse("tag:example.com,2005-01-01:test/tag#f")
    >>> str(tag_uri)
    'tag:example.com,2005-01-01:test/tag#f'

    >>> maker = TagURI.maker("example.com")
    >>> tag_uri = maker("test/2")
    >>> tag_uri.authority_name
    'example.com'
    >>> assert tag_uri.date == datetime.date.today()
    >>> tag_uri.specific
    'test/2'
    """

    tagging_entity: TaggingEntity
    specific: str
    fragment: str | None

    scheme: ClassVar[str] = "tag"

    def __str__(self) -> str:
        specific = self.specific
        fragment = self.fragment is not None and "#" + self.fragment or ""
        return f"{self.scheme}:{self.tagging_entity}:{specific}{fragment}"

    def as_dict(self) -> TagURIDict:
        """Return the tag URI as a dictionary."""
        return {
            "scheme": self.scheme,
            "tagging_entity": {
                "authority_name": self.tagging_entity.authority_name,
                "date": str(self.tagging_entity.date),
            },
            "specific": self.specific,
            "fragment": self.fragment,
        }

    @property
    def authority_name(self) -> str:
        return self.tagging_entity.authority_name

    @property
    def date(self) -> Date:
        return self.tagging_entity.date

    @property
    def time(self) -> datetime.date:
        return self.tagging_entity.time

    @classmethod
    def parse(cls, uri_str: str) -> TagURI:
        tree = parser().parse(uri_str)
        return TagTransformer().transform(tree)

    @classmethod
    def maker(cls, authority: str):
        def maker(
            specific: str,
            fragment: str | None = None,
            date: (
                datetime.date | datetime.datetime | DateThunk
            ) = lambda: datetime.datetime.now(tz=UTC).date(),
        ) -> TagURI:
            d: datetime.date
            match date:
                case DateThunk():
                    d = date()
                case datetime.datetime():
                    d = date.date()
                case datetime.date():
                    d = date
                case _:
                    raise TypeError("Unknown date")
            assert isinstance(d, datetime.date)
            tagging_entity = TaggingEntity(authority, d)
            return cls(tagging_entity, specific, fragment)

        assert isinstance(authority, str)
        return maker


__all__ = ["TagURI"]


class TaggingEntityDict(TypedDict):
    authority_name: str
    date: str


class TagURIDict(TypedDict):
    scheme: str
    tagging_entity: TaggingEntityDict
    specific: str
    fragment: str | None


@runtime_checkable
class DateThunk(Protocol):
    """Callable that takes no args and returns a datetime.date."""

    def __call__(self) -> datetime.date:
        ...  # pragma: no cover


@cache
def parser() -> lark.Lark:
    """Produce the Lark parser instance from our grammar."""
    grammar = _files.joinpath("grammar.lark").open()
    return lark.Lark(grammar, lexer="dynamic")


_files = importlib.resources.files("tag_uri")


class Year(int):
    """An ISO 8601 formatted four-digit year."""

    def __str__(self):
        return f"{self:04d}"


@dataclass(frozen=True, order=True, slots=True)
class Month:
    """An ISO 8601 formatted four-digit year with two-digit month."""

    year: Year
    month: int

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02d}"


@dataclass(frozen=True, order=True, slots=True)
class InvalidDate:
    """A date parsed from a tag URI but that is invalid in its integer ranges."""

    year: Year
    month: int
    day: int

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02d}-{self.day:02d}"


Date = Year | Month | InvalidDate | datetime.date


@total_ordering
@dataclass(frozen=True, slots=True)
class TaggingEntity:
    """The entity issuing the tag. Identified by a domain name or email and a date."""

    authority_name: str
    date: Date

    def __post_init__(self):
        if not self.authority_name:
            raise ValueError("authority_name must be non-empty")

    @property
    def time(self) -> datetime.date:
        match self.date:
            case Year():
                return datetime.date(self.date, 1, 1)
            case Month():
                return datetime.date(self.date.year, self.date.month, 1)
            case InvalidDate():
                return datetime.date(self.date.year, self.date.month, self.date.day)
            case datetime.date():
                return self.date

    def __str__(self) -> str:
        return f"{self.authority_name},{self.date}"

    def __lt__(self, other: TaggingEntity):
        return (self.authority_name, self.time) < (other.authority_name, other.time)


class TagTransformer(lark.Transformer):
    """Transform nodes from the Lark parser into usable types."""

    def specific(self, chars: list[str]) -> str:
        """Join a list of PCHAR into a string."""
        s = "".join(chars)
        assert isinstance(s, str)
        return s

    fragment = specific

    # Just convert these node types into strings directly
    EMAIL_ADDRESS = DNS_NAME = PCHAR = str
    # Just convert these node types into integers directly.
    DAY = MONTH = YEAR = int

    def date(self, items: list[int]) -> Date:
        """Convert a list of up to 3 integers (or nulls) into a suitable date representation."""
        d: Date
        match items:
            case [
                int(year),
                int(month),
                int(day),
            ] if year > 0 and 1 <= month <= 12 and 1 <= day <= 31:
                d = datetime.date(year, month, day)
            case [int(year), int(month), int(day)]:
                d = InvalidDate(Year(year), month, day)
            case [int(year), int(month), *_]:
                d = Month(Year(year), month)
            case [int(year), *_]:
                d = Year(year)
            case _:  # pragma: no cover
                raise ValueError("unreachable")
        assert isinstance(d, (Year, Month, InvalidDate, datetime.date))
        return d

    def authority_name(self, items: list[str]) -> str:
        """Unnest the authority name, which is a list, to a scalar."""
        (item,) = items
        assert isinstance(item, str)
        return item

    def tagging_entity(self, items) -> TaggingEntity:
        """Convert the tagging authority string and date into a TaggingEntity."""
        tagging_authority, date = items
        assert isinstance(tagging_authority, str)
        assert isinstance(date, (Year, Month, InvalidDate, datetime.date))
        return TaggingEntity(tagging_authority, date)

    def tag_uri(self, items):
        """Bundle together all the components of a TagURI into an instance."""
        tagging_entity, specific, fragment = items
        assert isinstance(tagging_entity, TaggingEntity)
        assert isinstance(specific, str)
        assert isinstance(fragment, str | None)
        return TagURI(tagging_entity, specific, fragment)
