"""
Liam Thompson and Eleanor Washburn
DS3500 - HW5

File: test_assignta.py
Description: This file contains unit tests for the assignment objectives in the assignta.py
implementation. The tests focus on verifying the functionality of the `Calculator` class,
which is used to evaluate different assignment criteria based on data loaded by the `DataLoader` class.
"""
# Import needed libraries
import unittest
from assignta import Calculator, DataLoader

class TestAssignmentObjectives(unittest.TestCase):

    def setUp(self):
        # Create instances of DataLoader for different test cases against expected results
        data_loader1 = DataLoader("tas.csv", "sections.csv", "test1.csv")
        data_loader2 = DataLoader("tas.csv", "sections.csv", "test2.csv")
        data_loader3 = DataLoader("tas.csv", "sections.csv", "test3.csv")

        # Create instances of Calculator using the loaded data against expected results
        self.calculator1 = Calculator(data_loader1.solution, data_loader1.tas, data_loader1.sections)
        self.calculator2 = Calculator(data_loader2.solution, data_loader2.tas, data_loader2.sections)
        self.calculator3 = Calculator(data_loader3.solution, data_loader3.tas, data_loader3.sections)

    def test_overallocation(self):
        # Check the overallocation penalty for each test case against expected results
        self.assertEqual(self.calculator1.overallocation(), 37)
        self.assertEqual(self.calculator2.overallocation(), 41)
        self.assertEqual(self.calculator3.overallocation(), 23)

    def test_conflicts(self):
        # Check the number of time conflicts for each test case against expected results
        self.assertEqual(self.calculator1.conflicts(), 8)
        self.assertEqual(self.calculator2.conflicts(), 5)
        self.assertEqual(self.calculator3.conflicts(), 2)

    def test_undersupport(self):
        # Check the undersupport penalty for each test case against expected results
        self.assertEqual(self.calculator1.undersupport(), 1)
        self.assertEqual(self.calculator2.undersupport(), 0)
        self.assertEqual(self.calculator3.undersupport(), 7)

    def test_unwilling(self):
        # Check the number of unwilling assignments for each test case against expected results
        self.assertEqual(self.calculator1.unwilling(), 53)
        self.assertEqual(self.calculator2.unwilling(), 58)
        self.assertEqual(self.calculator3.unwilling(), 43)

    def test_unpreferred(self):
        # Check the number of unpreferred assignments for each test case against expected results
        self.assertEqual(self.calculator1.unpreferred(), 15)
        self.assertEqual(self.calculator2.unpreferred(), 19)
        self.assertEqual(self.calculator3.unpreferred(), 10)
