import pytest
from source.linear_search import linear_search

@pytest.mark.parametrize(
    "input_arr, target, expected",
    [
        ([10],10,0),([1,4,5,6,8,9], 9, 5),([1,2,3], 2, 1),([243,332,554,999],999,3)
    ]

)
def test_linear_search(input_arr, target, expected):
    assert linear_search(input_arr, target) == expected