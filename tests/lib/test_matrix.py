from aoc.lib.matrix import Matrix, Point

def test_matrix():
    t = """\
1234
5678"""

    m = Matrix.parse_matrix(t, conversion=int)
    print(str(m))

    assert m.get((0, 0)) == 1
    assert m.contains_point((0, 0))

    m = Matrix.empty_matrix(10, 10, 0)
    m.get((0, 0))