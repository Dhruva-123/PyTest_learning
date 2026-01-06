import pytest
from source.binary_search_recursive import binary_search_recursive

@pytest.mark.parametrize(
    "input_arr, target, expected",
    [
        ([10],10,0),([1,4,5,6,8,9], 9, 5),([1,2,3], 2, 1),([243,332,554,999],999,3)
    ]

)
def test_binary_search_recursive(input_arr, target, expected):
    assert binary_search_recursive(input_arr, target) == expected