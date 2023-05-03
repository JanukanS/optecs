from collections import UserDict
import unittest
from functools import singledispatchmethod
from uuid import uuid4

class ComponentDict(UserDict):
    
    def __init__(self,*args):
        intermDict = {}
        for comp in args:
            if type(comp) in intermDict:
                raise TypeError("Duplicate Type")
            intermDict[type(comp)] = comp
        super().__init__(intermDict)
    
    @singledispatchmethod
    def __contains__(self,item: type):
        return super().__contains__(item)
    
    @__contains__.register
    def _(self,item: tuple):
        state = True
        for subItem in item:
            state &= super().__contains__(subItem)
        return state

    def add(self, comp):
        if type(comp) in self.data:
            raise TypeError("Duplicate Type")
        self.data[type(comp)] = comp

class EntityDict(UserDict):

    def __init__(self,compDictList = []):
        intermDict = {uuid4():compDict for compDict in compDictList}
        super().__init__(intermDict)

    def add(self, compDict):
        super().__setitem__(uuid4(), compDict)

    def query(self, compTuple):
        keyList = []
        for key, compDict in self.data.items():
            if compTuple in compDict:
                keyList.append(key)
        return keyList

class TestComponentDict(unittest.TestCase):
    def test_InitSucess(self):
        testCompDict = ComponentDict(1,True,8.8)
        self.assertEqual(testCompDict[int],1)
        self.assertEqual(testCompDict[bool], True)
        self.assertEqual(testCompDict[float],8.8)

    def test_InitFail(self):
        with self.assertRaises(TypeError):
            ComponentDict(1,2)

    def test_AddSuccess(self):
        testCompDict = ComponentDict(1)
        testCompDict.add(3.3)
        self.assertEqual(testCompDict[float],3.3)

    def test_AddFailure(self):
        testCompDict = ComponentDict(1)
        with self.assertRaises(TypeError):
            testCompDict.add(2)

    def test_HasItemTypes(self):
        testCompDict = ComponentDict(1,2.2)
        self.assertTrue(int in testCompDict)
        self.assertTrue(float in testCompDict)
        self.assertTrue((int, float) in testCompDict)

class TestEntityDict(unittest.TestCase):
    compDictList = [ComponentDict(1,2.2,True),
                    ComponentDict("strTest",False)]
    def test_InitSuccess(self):
        testEntDict = EntityDict(self.compDictList)
        self.assertEqual(len(testEntDict),len(self.compDictList))

    def test_AddSuccess(self):
        testEntDict = EntityDict()
        self.assertEqual(len(testEntDict),0)
        testEntDict.add(self.compDictList[0])
        self.assertEqual(len(testEntDict),1)
        testKey = list(testEntDict.keys())[0]
        self.assertEqual(testEntDict[testKey], self.compDictList[0])
