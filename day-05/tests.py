from main import Span as S, merge

assert S(0, 10).overlaps(S(5, 15))
assert S(5, 15).overlaps(S(0, 10))
assert S(0, 10).overlaps(S(10, 15))  # ranges are inclusive
assert S(0, 10).overlaps(S(4, 5)) # other entirely contained
assert S(4, 5).overlaps(S(0, 10)) # self entirely contained
assert not S(0, 10).overlaps(S(11, 15))
assert not S(11, 15).overlaps(S(0, 10))
assert not S(0, 4).overlaps(S(10, 14))
assert len(S(3, 5)) == 3
assert len(S(5, 3)) == 3


assert merge(S(0, 1), []) == [S(0, 1)]
assert merge(S(0, 1), [S(0, 1)]) == [S(0, 1)]
assert merge(S(0, 1), [S(0, 5)]) == [S(0, 5)]
assert merge(S(0, 1), [S(5, 7)]) == [S(5, 7), S(0, 1)]

# adjacent spans don't get merged
assert merge(S(0, 1), [S(2, 3)]) == [S(2, 3), S(0, 1)]

# but this doesn't affect total length
assert len(S(2, 3)) + len(S(0, 1)) == len(S(0, 3))

# introduced span should collapse the existing two spans
assert merge(S(3, 8), [S(0, 4), S(7, 10)]) == [S(0, 10)]

# introduced span should collapse 3 spans
assert merge(S(3, 16), [S(0, 4), S(7, 10), S(15, 20)]) == [S(0, 20)]

# introduced span should collapse 3 spans
assert merge(S(3, 16), [S(0, 4), S(7, 10), S(15, 20), S(25, 30)]) == [
    S(25, 30),
    S(0, 20),
]
