from collections import UserDict
import unittest
from functools import singledispatchmethod

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
