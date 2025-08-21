from src.basics.list_utils import flatten_list, remove_duplicates


def test_flatten_list() -> None:
    nested = [1, [2, [3, 4]], 5]
    assert flatten_list(nested) == [1, 2, 3, 4, 5]


def test_remove_duplicates() -> None:
    result = remove_duplicates([1, 2, 2, 3, 1])
    assert sorted(result) == [1, 2, 3]
