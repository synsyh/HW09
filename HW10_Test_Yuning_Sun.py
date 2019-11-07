"""
SSW810-HW10_Test_Yuning_Sun by Yuning Sun
4:06 下午 11/6/19
Module documentation: 
"""

import unittest

from HW10_Yuning_Sun import Repository


class TestRepository(unittest.TestCase):
    def test_repository(self):
        # create valid input
        sit = Repository('SIT_HW10')
        pt_student = sit.pretty_print('student')
        student_list, instructor_list, majors_list = [], [], []
        for student in sit.students:
            student_list.append([student.cwid, student.name, student.major, student.courses_completed,
                                 student.courses_required, student.courses_electives])
        for instructor in sit.instructors:
            for course in instructor.students.keys():
                # add rows according to courses
                instructor_list.append(
                    [instructor.cwid, instructor.name, instructor.dept, course, instructor.students[course]])
        for major, courses in sit.majors.items():
            majors_list.append([major, sorted(courses['R']), sorted(courses['E'])])
        self.assertEqual(student_list, [
            [10103, 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], None],
            [10115, 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], None],
            [10172, 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'],
             ['CS 501', 'CS 513', 'CS 545']],
            [10175, 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'],
             ['CS 501', 'CS 513', 'CS 545']],
            [10183, 'Chapman, O', 'SFEN', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],
             ['CS 501', 'CS 513', 'CS 545']],
            [11399, 'Cordova, I', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], None],
            [11461, 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'],
             ['SSW 540', 'SSW 565', 'SSW 810']],
            [11658, 'Kelly, P', 'SYEN', [], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']],
            [11714, 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'],
             ['SSW 540', 'SSW 565', 'SSW 810']],
            [11788, 'Fuller, E', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], None]]
                         )
        self.assertEqual(instructor_list,
                         [[98765, 'Einstein, A', 'SFEN', 'SSW 567', 4], [98765, 'Einstein, A', 'SFEN', 'SSW 540', 3],
                          [98764, 'Feynman, R', 'SFEN', 'SSW 564', 3], [98764, 'Feynman, R', 'SFEN', 'SSW 687', 3],
                          [98764, 'Feynman, R', 'SFEN', 'CS 501', 1], [98764, 'Feynman, R', 'SFEN', 'CS 545', 1],
                          [98763, 'Newton, I', 'SFEN', 'SSW 555', 1], [98763, 'Newton, I', 'SFEN', 'SSW 689', 1],
                          [98760, 'Darwin, C', 'SYEN', 'SYS 800', 1], [98760, 'Darwin, C', 'SYEN', 'SYS 750', 1],
                          [98760, 'Darwin, C', 'SYEN', 'SYS 611', 2], [98760, 'Darwin, C', 'SYEN', 'SYS 645', 1]]
                         )
        self.assertEqual(majors_list,
                         [['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']],
                          ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]]
                         )
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


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
