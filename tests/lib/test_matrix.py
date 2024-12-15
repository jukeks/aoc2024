from aoc.lib.matrix import Matrix, Point

def test_matrix():
    t = """\
12
34"""

    m = Matrix.parse_matrix(t, conversion=int)
    print(str(m))

    assert m.get((0, 0)) == 1
    assert m.get((1, 0)) == 2
    assert m.get((0, 1)) == 3
    assert m.get((1, 1)) == 4
    assert m.contains_point((0, 0))

    for a, b in zip(m, [[1, 2], [3, 4]]):
        assert a == b

    m = Matrix.empty_matrix(10, 10, 0)
    m.get((0, 0))