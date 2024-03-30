# ruff: noqa: UP006
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    ForwardRef,
    Optional,
    TypedDict,
    TypeVar,
    Union,
    get_type_hints,
)

import pytest
from type_lens import TypeView
from typing_extensions import NotRequired, Required

if TYPE_CHECKING:
    from typing import Final


T = TypeVar("T")


def _check_parsed_type(type_lens: TypeView, expected: dict[str, Any]) -> None:
    __tracebackhide__ = True
    for key, expected_value in expected.items():
        lens_value = getattr(type_lens, key)
        if lens_value != expected_value:
            pytest.fail(f"Expected {key} to be {expected_value}, got {lens_value} instead. TypeLens: {type_lens}")


_type_lens_int: Final = TypeView(int)


class _TD(TypedDict):
    req_int: Required[int]
    req_list_int: Required[list[int]]
    not_req_int: NotRequired[int]
    not_req_list_int: NotRequired[list[int]]
    ann_req_int: Required[Annotated[int, "foo"]]
    ann_req_list_int: Required[Annotated[list[int], "foo"]]


_typed_dict_hints: Final = get_type_hints(_TD, include_extras=True)


@pytest.mark.parametrize(
    ("annotation", "expected"),
    [
        (
            int,
            {
                "raw": int,
                "annotation": int,
                "origin": None,
                "args": (),
                "metadata": (),
                "is_annotated": False,
                "is_required": False,
                "is_not_required": False,
                "inner_types": (),
            },
        ),
        (
            list[int],
            {
                "raw": list[int],
                "annotation": list[int],
                "origin": list,
                "args": (int,),
                "metadata": (),
                "is_annotated": False,
                "is_required": False,
                "is_not_required": False,
                "inner_types": (TypeView(int),),
            },
        ),
        (
            Annotated[int, "foo"],
            {
                "raw": Annotated[int, "foo"],
                "annotation": int,
                "origin": None,
                "args": (),
                "metadata": ("foo",),
                "is_annotated": True,
                "is_required": False,
                "inner_types": (),
            },
        ),
        (
            Annotated[list[int], "foo"],
            {
                "raw": Annotated[list[int], "foo"],
                "annotation": list[int],
                "origin": list,
                "args": (int,),
                "metadata": ("foo",),
                "is_annotated": True,
                "is_required": False,
                "is_not_required": False,
                "inner_types": (TypeView(int),),
            },
        ),
        (
            _typed_dict_hints["req_int"],
            {
                "raw": _typed_dict_hints["req_int"],
                "annotation": int,
                "origin": None,
                "args": (),
                "metadata": (),
                "is_annotated": False,
                "is_required": True,
                "is_not_required": False,
                "inner_types": (),
            },
        ),
        (
            _typed_dict_hints["req_list_int"],
            {
                "raw": _typed_dict_hints["req_list_int"],
                "annotation": list[int],
                "origin": list,
                "args": (int,),
                "metadata": (),
                "is_annotated": False,
                "is_required": True,
                "is_not_required": False,
                "inner_types": (TypeView(int),),
            },
        ),
        (
            _typed_dict_hints["not_req_int"],
            {
                "raw": _typed_dict_hints["not_req_int"],
                "annotation": int,
                "origin": None,
                "args": (),
                "metadata": (),
                "is_annotated": False,
                "is_required": False,
                "is_not_required": True,
                "inner_types": (),
            },
        ),
        (
            _typed_dict_hints["not_req_list_int"],
            {
                "raw": _typed_dict_hints["not_req_list_int"],
                "annotation": list[int],
                "origin": list,
                "args": (int,),
                "metadata": (),
                "is_annotated": False,
                "is_required": False,
                "is_not_required": True,
                "inner_types": (TypeView(int),),
            },
        ),
        (
            _typed_dict_hints["ann_req_int"],
            {
                "raw": _typed_dict_hints["ann_req_int"],
                "annotation": int,
                "origin": None,
                "args": (),
                "metadata": ("foo",),
                "is_annotated": True,
                "is_required": True,
                "is_not_required": False,
                "inner_types": (),
            },
        ),
        (
            _typed_dict_hints["ann_req_list_int"],
            {
                "raw": _typed_dict_hints["ann_req_list_int"],
                "annotation": list[int],
                "origin": list,
                "args": (int,),
                "metadata": ("foo",),
                "is_annotated": True,
                "is_required": True,
                "is_not_required": False,
                "inner_types": (TypeView(int),),
            },
        ),
    ],
)
def test_parsed_type_from_annotation(annotation: Any, expected: dict[str, Any]) -> None:
    """Test ParsedType.from_annotation."""
    _check_parsed_type(TypeView(annotation), expected)


def test_parsed_type_from_union_annotation() -> None:
    """Test ParsedType.from_annotation for Union."""
    annotation = Union[int, list[int]]
    expected = {
        "raw": annotation,
        "annotation": annotation,
        "origin": Union,
        "args": (int, list[int]),
        "metadata": (),
        "is_annotated": False,
        "is_required": False,
        "is_not_required": False,
        "inner_types": (TypeView(int), TypeView(list[int])),
    }
    _check_parsed_type(TypeView(annotation), expected)


@pytest.mark.parametrize("value", ["int", ForwardRef("int")])
def test_parsed_type_is_forward_ref_predicate(value: Any) -> None:
    """Test ParsedType with ForwardRef."""
    parsed_type = TypeView(value)
    assert parsed_type.is_forward_ref is True
    assert parsed_type.annotation == value
    assert parsed_type.origin is None
    assert parsed_type.args == ()
    assert parsed_type.metadata == ()
    assert parsed_type.is_annotated is False
    assert parsed_type.is_required is False
    assert parsed_type.is_not_required is False
    assert parsed_type.inner_types == ()


def test_parsed_type_is_type_var_predicate() -> None:
    """Test ParsedType.is_type_var."""
    assert TypeView(int).is_type_var is False
    assert TypeView(T).is_type_var is True
    assert TypeView(Union[int, T]).is_type_var is False  # pyright: ignore[reportGeneralTypeIssues]


def test_parsed_type_is_union_predicate() -> None:
    """Test ParsedType.is_union."""
    assert TypeView(int).is_union is False
    assert TypeView(Optional[int]).is_union is True
    assert TypeView(Union[int, None]).is_union is True
    assert TypeView(Union[int, str]).is_union is True


def test_parsed_type_is_optional_predicate() -> None:
    """Test ParsedType.is_optional."""
    assert TypeView(int).is_optional is False
    assert TypeView(Optional[int]).is_optional is True
    assert TypeView(Union[int, None]).is_optional is True
    assert TypeView(Union[int, None, str]).is_optional is True
    assert TypeView(Union[int, str]).is_optional is False


def test_parsed_type_is_subclass_of() -> None:
    """Test ParsedType.is_type_of."""
    assert TypeView(bool).is_subclass_of(int) is True
    assert TypeView(bool).is_subclass_of(str) is False
    assert TypeView(Union[int, str]).is_subclass_of(int) is False
    assert TypeView(list[int]).is_subclass_of(list) is True
    assert TypeView(list[int]).is_subclass_of(int) is False
    assert TypeView(Optional[int]).is_subclass_of(int) is False
    assert TypeView(Union[bool, int]).is_subclass_of(int) is True


def test_parsed_type_has_inner_subclass_of() -> None:
    """Test ParsedType.has_type_of."""
    assert TypeView(list[int]).has_inner_subclass_of(int) is True
    assert TypeView(list[int]).has_inner_subclass_of(str) is False
    assert TypeView(list[Union[int, str]]).has_inner_subclass_of(int) is False


def test_parsed_type_equality() -> None:
    assert TypeView(int) == TypeView(int)
    assert TypeView(int) == TypeView(Annotated[int, "meta"])
    assert TypeView(int) != int
    assert TypeView(list[int]) == TypeView(list[int])
    assert TypeView(list[int]) != TypeView(list[str])
    assert TypeView(list[str]) != TypeView(tuple[str])
    assert TypeView(Optional[str]) == TypeView(Union[str, None])
