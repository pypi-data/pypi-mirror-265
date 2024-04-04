"""Tests for the potoroo package."""

from __future__ import annotations

from eris import ErisResult, Err, Ok

from potoroo import Repo, TaggedRepo


class FakeDB(Repo[int, str]):
    """Fake database."""

    def __init__(self) -> None:
        self._keys = list(range(100))
        self._db: dict[int, str] = {}

    def add(self, some_item: str, /, *, key: int = None) -> ErisResult[int]:
        """Fake add."""
        key = self._keys.pop(0)
        self._db[key] = some_item
        return Ok(key)

    def get(self, key: int) -> ErisResult[str | None]:
        """Fake get."""
        return Ok(self._db[key])

    def remove(self, item: str, /) -> ErisResult[str | None]:
        """Fake remove."""
        item_key = None
        for key, value in self._db.items():
            if value == item:
                item_key = key
                break
        else:
            return Err(f"Unable to find item | {item=}")
        return Ok(self._db.pop(item_key))

    def all(self) -> ErisResult[list[str]]:
        """Fake all."""
        return Ok(sorted(self._db.values()))


class FakeTaggedDB(FakeDB, TaggedRepo[int, str, str]):
    """Fake tagged database."""

    def get_by_tag(self, tag: str) -> ErisResult[list[str]]:
        """Fake get_by_tag."""
        return Ok([v for v in self._db.values() if tag in v])


def test_repo() -> None:
    """Test the Repo type."""
    db = FakeDB()
    foo_idx = db.add("foo").unwrap()
    baz_idx = db.add("baz").unwrap()
    assert db.get(foo_idx).unwrap() == "foo"
    assert db.update(foo_idx, "bar").unwrap() == "foo"
    assert db.remove("bar").unwrap() == "bar"
    assert db.remove_by_key(baz_idx).unwrap() == "baz"


def test_tagged_repo() -> None:
    """Test the TaggedRepo type."""
    db = FakeTaggedDB()
    foo_idx = db.add("foo").unwrap()
    db.add("bar").unwrap()
    db.add("baz").unwrap()

    assert db.get(foo_idx).unwrap() == "foo"
    assert db.get_by_tag("f").unwrap() == ["foo"]
    assert db.all().unwrap() == ["bar", "baz", "foo"]
    assert db.remove_by_tag("b").unwrap() == ["bar", "baz"]
