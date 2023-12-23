# vi:ai:sw=4 ts=4 et

import json
from typing import Any, Dict, List, Optional, Tuple

class Trie:
    def __init__(self, key: Optional[str] = None, value: Optional[Any] = None):
        self.key = None if key is None or len(key) == 0 else key
        self.value = value
        self.children: Dict[str,Trie] = {}

    def add(self, key: str, value: Any):
        # attach a value to this node
        if len(key) == 0:
            assert self.value is None
            self.value = value
            return

        # compress prefix if possible
        if self.key is None and len(self.children) == 0:
            self.key = key
            self.value = value
            return

        # push the value down the trie
        if key[0] in self.children:
            self.children[key[0]].add(key[1:], value)
            return

        # add a new subtrie
        child = Trie(key[1:], value)
        self.children[key[0]] = child

        # do we need to expand the compressed prefix?
        if self.key and key[0] == self.key[0] and len(self.key) > 1:
            child.add(self.key[1:], self.value)
            self.key = None
            self.value = None

    def __getitem__(self, key: str):
        if key == self.key:
            return self.value

        try:
            if len(key) > 0 and key[0] in self.children:
                child = self.children[key[0]]
                return child[key[1:]]
        except KeyError:
            pass  # handle as below, so the caller gets the whole key

        raise KeyError(key)

    def __contains__(self, key: str):
        try:
            self.__getitem__(key)
        except KeyError:
            return False

        return True

    def toJSON(self) -> Dict:
        children = dict((k, v.toJSON()) for k, v in self.children.items())
        return {"key": self.key, "value": self.value, "children": children}

    def __str__(self) -> str:
        return json.dumps(self.toJSON())

class Iterator:
    def __init__(self, root:Trie):
        self.root = root
        self.prefix = []
        self.cursor: Trie = root
        self.index: Optional[int] = 0 if root.key else None

    def advance(self, token:str) -> bool:
        if self.index is not None: # check compressed prefix
            if self.index == len(self.cursor.key):
                return False # dropped off the end
            if self.cursor.key[self.index] == token:
                self.index += 1
                self.prefix.append(token)
                return True
            else: # compressed prefix didn't match
                self.index = None

        if token in self.cursor.children:
            self.cursor = self.cursor.children[token]
            self.prefix.append(token)
            if self.cursor.key:
                self.index = 0
            return True

        return False

    def value(self) -> Optional[Any]:
        if self.index is not None and self.index < len(self.cursor.key):
            return None
        return self.cursor.value

    def key(self) -> str:
        return ''.join(self.prefix)
        

class Searcher:
    def __init__(self, root:Trie):
        self.root = root
        self.echelon = []

    def advance(self, token:str):
        next_echelon = [i for i in self.echelon if i.advance(token)]
        begin = Iterator(self.root)
        if begin.advance(token):
            next_echelon.append(begin)
        self.echelon = next_echelon

    def value(self) -> Optional[Tuple[str,Any]]:
        for i in self.echelon:
            ov = i.value()
            if ov is not None:
                return (i.key(), ov)
        return None
