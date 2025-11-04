from tp_algos.structures.union_find import UnionFind

def test_union_find():
    uf = UnionFind(5)
    assert uf.union(0, 1)
    assert uf.union(3, 4)
    assert uf.find(0) == uf.find(1)
    assert uf.find(3) == uf.find(4)
    assert uf.union(1, 4)
    assert uf.find(0) == uf.find(3)
