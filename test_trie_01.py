# vi:ai:sw=4 ts=4 et
from trie_01 import Trie, Searcher

import pdb

def test_trivial():
    t = Trie('a', 1)
    assert ('a' in t) == True
    assert t['a'] == 1
    assert ('b' in t) == False
    assert ('ab' in t) == False

def test_forked():
    t = Trie('abba', 1)
    assert ('abba' in t) == True
    assert t['abba'] == 1

    t.add('abra', 2)
    assert ('abba' in t) == True
    assert t['abba'] == 1
    assert ('abra' in t) == True
    assert t['abra'] == 2

    t.add('cadabra', 3)
    assert ('abba' in t) == True
    assert t['abba'] == 1
    assert ('abra' in t) == True
    assert t['abra'] == 2
    assert ('cadabra' in t) == True
    assert t['cadabra'] == 3

    print(t)

def test_rooted():
    t = Trie(None, None)

    t.add('abra', 2)
    assert ('abra' in t) == True
    assert t['abra'] == 2

    t.add('cadabra', 3)
    assert ('abra' in t) == True
    assert t['abra'] == 2
    assert ('cadabra' in t) == True
    assert t['cadabra'] == 3

    ## we seem to have a problem with common prefixes ...
   #t.add('abracadabra', 5)
   #assert ('abra' in t) == True
   #assert t['abra'] == 2
   #assert ('cadabra' in t) == True
   #assert t['cadabra'] == 3
   #assert ('abracadabra' in t) == True
   #assert t['abracadabra'] == 3

    print(t)

def test_search():
    t = Trie('abba', 1)
    t.add('abra', 2)
    t.add('cadabra', 3)

    s = Searcher(t)
    #pdb.set_trace()
    for c in 'abb':
        s.advance(c)
        assert s.value() is None
    s.advance('a')
    assert s.value() == ('abba', 1)

    s = Searcher(t)
    for c in 'abrupt cadaver abbreviated abr':
        s.advance(c)
        assert s.value() is None
    s.advance('a')
    assert s.value() == ('abra', 2)
    
    
if __name__ == "__main__":
    test_trivial()
    test_forked()
    test_rooted()
    test_search()
