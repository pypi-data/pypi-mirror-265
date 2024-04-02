from __future__ import annotations

import dataclasses
import logging
from typing import IO, Any, Callable, ClassVar, Iterable

from typing_extensions import TypedDict
from werkzeug.datastructures import FileStorage

from ckan import types

log = logging.getLogger(__name__)

strategies: dict[str, type[ExtractionStrategy]] = {}

Storage = FileStorage


class RecordOptions(TypedDict, total=False):
    """Options for Record extracted by Strategy."""

    # trigger an update if the data produced by the record already exists
    update_existing: bool

    # return more details after producing the data
    verbose: bool

    # custom options that are not stabilized yet
    extras: dict[str, Any]


class StrategyOptions(TypedDict, total=False):
    """Options for Strategy."""

    # options passed into every record produced by the strategy
    record_options: RecordOptions

    # function that returns a file from source using its name. Can be used to
    # refer files in archive when creating a resource record with uploaded
    # file, for example.
    locator: Callable[..., Any]

    # strategy that should be used for nested sources. For example, for files
    # inside an archivecd
    nested_strategy: str

    # custom options that are not stabilized yet
    extras: dict[str, Any]


class IngestionResult(TypedDict, total=False):
    """Outcome of the record ingestion."""

    # created/updated data
    result: Any
    # indicator of successful ingestion
    success: bool
    # additional details about ingestion
    details: dict[str, Any]


@dataclasses.dataclass
class Record:
    """Single element produced by extraction strategy.

    The record is responsible for creating/updating the data.
    """

    # original data extracted by strategy
    raw: dict[str, Any]

    # transformed data adapted to the record needs
    data: dict[str, Any] = dataclasses.field(init=False)

    # options received from extraction strategy
    options: RecordOptions = dataclasses.field(default_factory=RecordOptions)

    def __post_init__(self):
        self.data = self.transform(self.raw)

    def transform(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Transform arbitrary data into a data that has sense for a record."""
        return raw

    def fill(self, defaults: dict[str, Any], overrides: dict[str, Any]):
        """Apply default and overrides to the data."""
        self.data = {**defaults, **self.data, **overrides}

    def ingest(self, context: types.Context) -> IngestionResult:
        """Create/update something using the data."""
        log.debug("No-op ingestion: %s", self.data)

        return {"success": True, "result": None, "details": {}}


class ExtractionStrategy:
    """Record extraction strategy.

    This class is repsonsible for parsing the source and yielding record
    instances from it.

    Attributes:
        mimetypes: collection of mimetypes supported by the strategy
    """

    mimetypes: ClassVar[set[str]] = set()
    record_factory: type[Record] = Record

    @classmethod
    def can_handle(cls, mime: str | None, source: Storage) -> bool:
        """Check if strategy can handle given mimetype/source."""
        return mime in cls.mimetypes

    @classmethod
    def must_handle(cls, mime: str | None, source: Storage) -> bool:
        """Check if strategy is the best choice for handling given mimetype/source."""
        return False

    def chunks(self, source: Storage, options: StrategyOptions) -> Iterable[Any]:
        """Iterate over separate chunks of data with correpoinding options
        suitable for Record creation."""
        return []

    def chunk_into_record(self, chunk: Any, options: StrategyOptions) -> Record:
        return self.record_factory(
            chunk,
            options.get("record_options", RecordOptions()),
        )

    def extract(
        self,
        source: Storage,
        options: StrategyOptions,
    ) -> Iterable[Record]:
        """Return iterable over all records extracted from source.

        `opptions` contains settings, helpers and other artifacts that can help
        during extraction. It's passed by user or generated/modified by other
        strategies, so there are no guarantees or rules when you are using it.

        """
        for chunk in self.chunks(source, options):
            yield self.chunk_into_record(chunk, options)


def get_handler_for_mimetype(
    mime: str | None,
    source: Storage,
) -> ExtractionStrategy | None:
    """Select the most suitable handler for the MIMEType.

    The first strategy that `must_handle` is returned. If there is no such
    strategy, the first that `can_handle` is returned.

    """
    choices: list[type[ExtractionStrategy]] = []
    for strategy in strategies.values():
        if not strategy.can_handle(mime, source):
            continue

        if strategy.must_handle(mime, source):
            return strategy()

        choices.append(strategy)

    if choices:
        return choices[0]()

    return None


def make_storage(
    stream: IO[bytes],
    name: str | None = None,
    mimetype: str | None = None,
):
    return Storage(stream, name, content_type=mimetype)
