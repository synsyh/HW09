"""
SSW810-HW09_Test_Yuning_Sun by Yuning Sun
9:47 下午 10/29/19
Module documentation: 
"""
import unittest

from HW09.HW09_Yuning_Sun import Repository


class TestRepository(unittest.TestCase):
    def test_repository(self):
        # create valid input
        sit = Repository('sit')
        # validation
        self.assertEqual(len(sit.instructors), 6)
        self.assertEqual(len(sit.students), 10)
        self.assertEqual(sit.find_people(98765, 'instructor').name, 'Einstein, A')
        self.assertEqual(sit.find_people(98765, 'instructor').dept, 'SFEN')
        self.assertEqual(sit.find_people(98765, 'instructor').students, {'SSW 567': 4, 'SSW 540': 3, 'SSW 541': 1})
        self.assertEqual(sit.find_people(11788, 'student').name, 'Fuller, E')
        self.assertEqual(sit.find_people(11788, 'student').major, 'SYEN')
        self.assertEqual(sit.find_people(11788, 'student').courses['SSW 540'], 'A')
        self.assertEqual(sit.find_people(11788, 'student').courses['SSW 541'], '')
        # Pretty print must choose from student or instructor
        with self.assertRaises(ValueError):
            sit.pretty_print('professor')
        # NYU is an empty directory
        with self.assertRaises(FileNotFoundError):
            Repository('NYU')
        # CU is a directory which has grades and instructors but not students
        with self.assertRaises(FileNotFoundError):
            Repository('CU')
        # YNU has all files, which is same as sit, except YNU lacks a instructor
        # So when program processes grades, it can not find related instructor and raises ValueError
        # When lacks a student, it will raise ValueError too.
        with self.assertRaises(ValueError):
            Repository('YNU')
        # MIT has all files, but one of its instructors has a cwid which is 9876a5
        # So when program processing, it can not transform it to int and raises ValueError
        with self.assertRaises(ValueError):
            Repository('MIT')
        # ST has a grades file that includes a student not included in students.txt file
        # and an instructor that is not in the instructors file.
        with self.assertRaises(ValueError):
            Repository('ST')
        # BU has a grades file that has the wrong values
        with self.assertRaises(ValueError):
            Repository('BU')
