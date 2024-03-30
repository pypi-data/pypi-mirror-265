#!/usr/bin/env python3
from __future__ import annotations

from typing import Mapping, Collection, Any, Iterator
from collections import UserDict
from collections.abc import Set, KeysView, ItemsView, ValuesView


# A custom "key" for a Thick dict.
# Effectively a frozenset implementation
# Except for a custom repr
class ThickKey(Set):
    # Should be identical to a frozenset except for the __repr__
    def __init__(self, d: Collection) -> None:
        if isinstance(d, str) and len(d) > 1:
            d = (d,)
        self.data: frozenset[Any] = frozenset(d)
        super().__init__()

    def __contains__(self, key: Any) -> bool:
        return key in self.data

    def __iter__(self) -> Iterator[Any]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __hash__(self) -> int:
        return self._hash()

    def __repr__(self) -> str:
        # This makes the Thick*Views look better
        return str(tuple(self.data))


# A Thick dict. Rather than growing downward (getting "longer"),
# it grows outward (getting "Thicker").
# In a normal dict, if you want to map "a" to "foo" and also "b" to "foo",
# This looks like:
# example_dict = {
#   "a": "foo",
#   "b": "foo",
# }
#
# In a Thick dict, this looks instead like:
# example_thick = Thick({
# ("a", "b"): "foo"
# })
# But this key isn't just a tuple:
# example_thick["a"]
# > "foo"
# example_thick["b"]
# > "foo"
# example_thick[("a", "b")]
# > "foo"
class Thick(UserDict):
    #####################################
    # Modified from collections.UserDict
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def __init__(self, input_dict: Mapping | None = None, /, **kwargs) -> None:
        # Because of a custom "update" method (as used in UserDict)
        # This still creates a valid Thick dict
        super().__init__(input_dict, **kwargs)

    def __or__(self, other: Any) -> Thick:
        if isinstance(other, UserDict | dict | Thick):
            new: Thick = self.copy()
            new.update(other)
            return new
        return NotImplemented

    def __ror__(self, other: Any) -> Thick:
        if isinstance(other, UserDict | dict | Thick):
            new: Thick = self.copy()
            new.update(other)
            return new
        return NotImplemented

    def __ior__(self, other: Any) -> Thick:
        if isinstance(other, UserDict | Thick | dict):
            k: Any
            v: Any
            for k, v in other.items():
                self[k] = v
            return self
        return NotImplemented

    def copy(self) -> Thick:
        if self.__class__ is Thick:
            return Thick(self.data.copy())
        import copy

        data: dict[frozenset[Any], Any] = self.data
        try:
            self.data = {}
            c: Any = copy.copy(self)
        finally:
            self.data = data
        # If this looks like "c" could, somehow, be unbound
        # That's because this is a word-for-word copy of
        # the copy implementation of UserDict, except for
        # substituting "UserDict" for "Thick" and adding
        # type hints. ymmv on using subclasses of Thick (or UserDict)
        # with this.
        c.update(self)
        return c

    def __contains__(self, key: Any) -> bool:
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        return check_key in self.keys()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Modified from collections.UserDict
    #####################################
    # (ADAPTED FROM collections.abc.MutableMapping)
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def __getitem__(self, key: Any) -> Any:
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        if check_key in self.keys():
            whole_key: ThickKey = self.get_entire_key(check_key)
            return self.data[whole_key]

        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)

        raise KeyError(key)

    # This is by far the most "involved" method in this
    # data structure. The logic helps it ensure that it
    # retains the structure of having unique values.
    def __setitem__(self, key: Any, item: Any) -> None:
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        current_key: ThickKey
        current_value: Any
        # First, if the item is already in this
        if item in self.values():
            for current_key, current_value in self.items():
                if item == current_value:
                    # If the given key is not a subset of the current key
                    if not (check_key <= current_key):
                        # Create a new key as the union of the two
                        # Use only this key
                        # (The cast to ThickKey is technially redundant,
                        # But mypy complains otherwise)
                        new_key: ThickKey = ThickKey(current_key | check_key)
                        del self.data[current_key]
                        self.data[new_key] = current_value
                    return

        # Otherwise, the item is new
        else:
            mutable_new_key: set[Any]
            k: Any
            for current_key, current_value in self.items():
                # If the desired key is already partially (or fully)
                # In the keys
                if check_key <= current_key:
                    mutable_new_key = set(current_key)
                    # Remove all the desired values from the
                    # old key
                    for k in check_key:
                        mutable_new_key.remove(k)
                    del self.data[current_key]
                    # If there are still values in the old key,
                    # reset it
                    if len(mutable_new_key) > 0:
                        self.data[ThickKey(mutable_new_key)] = current_value
                    self.data[check_key] = item
                    return

                # This is what happens when there are overlapping items
                # but check_key is not a subset of current_key
                else:
                    # (The cast to ThickKey is technially redundant,
                    # But mypy complains otherwise)
                    key_intersection: ThickKey = ThickKey(check_key & current_key)
                    if len(key_intersection) != 0:
                        mutable_new_key = set(current_key)
                        # Remove any values in the intersection that are
                        # in the current_key
                        for k in key_intersection:
                            if k in mutable_new_key:
                                mutable_new_key.remove(k)

                        # The old version gets deleted
                        # The given check_key is set to the desired item
                        # The remaining values from the current_key are
                        # in new_key and set to the current_value
                        del self.data[check_key]
                        self.data[ThickKey(mutable_new_key)] = current_value
                        self.data[check_key] = item
                        return

        # If we've fallen through here, the value is not already in the Thick dict
        # And the given key has no intersection with any key already in the Thick dict
        # Thus, we just set the new value
        self.data[check_key] = item

    def __delitem__(self, key: Any) -> None:
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        if check_key in self.data:
            del self.data[check_key]
            return

        if check_key in self.keys():
            whole_key: ThickKey = self.get_entire_key(check_key)
            # (The cast to ThickKey is technially redundant,
            # But mypy complains otherwise)
            remaining_keys: ThickKey = ThickKey(whole_key - check_key)
            val: Any = self.data[whole_key]
            del self.data[whole_key]
            self.data[remaining_keys] = val
            return

        # If part of all of the check_key is not
        # already in the Thick dict, it's a key error
        raise KeyError(key)

    # Given a partial or whole key, return the entire ThickKey:
    def get_entire_key(self, key: Any) -> ThickKey:
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        current_key: ThickKey
        for current_key in self.keys():
            if check_key <= current_key:
                return current_key

        raise KeyError(key)

    # Given a key or a subset of a key, remove the entire
    # key and its value in one go
    def delete_entire_key(self, key: Any) -> None:
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        # If any part of it is there, remove the whole thing
        if check_key in self.keys():
            whole_key: ThickKey = self.get_entire_key(check_key)
            del self.data[whole_key]
            return

        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def values(self) -> ThickValuesView:
        return ThickValuesView(self)

    def keys(self) -> ThickKeysView:
        return ThickKeysView(self)

    def items(self) -> ThickItemsView:
        return ThickItemsView(self)


class ThickKeysView(KeysView):
    # Type Hint for mypy
    _mapping: Thick

    def __contains__(self, key: Any) -> bool:
        check_key: ThickKey
        if not isinstance(key, ThickKey):
            check_key = ThickKey(key)
        else:
            check_key = key

        # Rather than repeating logic, we do this once here:

        # It's probably more inefficient to check the whole key and then
        # check each key in turn. Using a <= with the sets, we can just do
        # one for-loop, O(n) in the size of the Thick dict.
        k: ThickKey
        for k in self._mapping.keys():
            if check_key <= k:
                return True

        return False

    # Similar to a dict_keys __repr__
    def __repr__(self):
        return f"{self.__class__.__name__}({list(self._mapping.data.keys())})"


class ThickValuesView(ValuesView):
    # Similar to a dict_values __repr__
    def __repr__(self):
        return f"{self.__class__.__name__}({list(self._mapping.data.values())})"


class ThickItemsView(ItemsView):
    # Similar to a dict_items __repr__
    def __repr__(self):
        return f"{self.__class__.__name__}({list(zip(self._mapping.data.keys(), self._mapping.data.values()))})"
