"""
SSW810-HW09_Yuning_Sun by Yuning Sun
7:54 下午 10/29/19
Module documentation: 
"""
import os
from collections import defaultdict
import prettytable


class Repository:
    def __init__(self, directory):
        # check if the file exists
        if not os.path.exists(directory):
            raise FileNotFoundError(f'{directory} not found')
        # create container
        self.directory = directory
        self.students = []
        self.instructors = []
        # parse the files
        self.parse_students()
        self.parse_instructors()
        self.parse_grades()

    def parse_students(self):
        # parse students.txt
        path = os.path.join(self.directory, 'students.txt')
        try:
            with open(path) as f:
                for line in f:
                    items = line.strip().split('\t')
                    # process files with the wrong number of fields
                    if len(items) != 3:
                        raise ValueError(f'can not process {line}')
                    try:
                        cwid = int(items[0])
                    except ValueError:
                        raise ValueError(f'can not transform {items[0]}')
                    # add data
                    student = Student(cwid)
                    student.name = items[1]
                    student.major = items[-1]
                    self.students.append(student)
        except FileNotFoundError:
            raise FileNotFoundError(f'file not found {path}')

    def parse_instructors(self):
        # parse instructors.txt
        path = os.path.join(self.directory, 'instructors.txt')
        try:
            with open(path) as f:
                for line in f:
                    items = line.strip().split('\t')
                    # process files with the wrong number of fields
                    if len(items) != 3:
                        raise ValueError(f'can not process {line}')
                    try:
                        cwid = int(items[0])
                    except ValueError:
                        raise ValueError(f'can not transform {items[0]}')
                    # add data
                    instructor = Instructor(cwid)
                    instructor.name = items[1]
                    instructor.dept = items[-1]
                    self.instructors.append(instructor)
        except FileNotFoundError:
            raise FileNotFoundError(f'file not found {path}')

    def parse_grades(self):
        # parse grades.txt
        path = os.path.join(self.directory, 'grades.txt')
        try:
            with open(path) as f:
                for line in f:
                    items = line.strip().split('\t')
                    # process files with the wrong number of fields
                    if len(items) != 4 and len(items) != 3:
                        raise ValueError(f'can not process {line}')
                    try:
                        cwid_student = int(items[0])
                        cwid_instructor = int(items[-1])
                    except ValueError:
                        raise ValueError(f'can not transform {items[0]} or {items[-1]}')
                    # add data
                    student = self.find_people(cwid_student, 'student')
                    # add grades
                    # if the student is in first semester, which means he only has course but not have grade
                    # then making his grade empty string
                    if student:
                        if len(items) == 4:
                            student.courses[items[1]] = items[2]
                        else:
                            student.courses[items[1]] = ''
                    else:
                        raise ValueError(f'can not find the student {cwid_student}')
                    # find instructor and add students
                    instructor = self.find_people(cwid_instructor, 'instructor')
                    if instructor:
                        instructor.students[items[1]] += 1
                    else:
                        raise ValueError(f'can not find the instructor {cwid_student}')
        except FileNotFoundError:
            raise FileNotFoundError(f'file not found {path}')

    def find_people(self, cwid, identity):
        """
        find student or instructor in repository
        :param cwid: cwid
        :param identity: student or instructor
        :return: an object of Student or Instructor
        """
        if identity == 'student':
            people_list = self.students
        elif identity == 'instructor':
            people_list = self.instructors
        else:
            raise ValueError(f'please enter students or instructors')
        for p in people_list:
            if p.cwid == cwid:
                return p
        return None

    def pretty_print(self, identity):
        """
        pretty print
        :param identity: student or instructor
        :return: pt object
        """
        if identity == 'student':
            pt = prettytable.PrettyTable(['CWID', 'Name', 'Completed Courses'])
            # add rows
            for student in self.students:
                pt.add_row([student.cwid, student.name, sorted(list(student.courses.keys()))])
        elif identity == 'instructor':
            pt = prettytable.PrettyTable(['CWID', 'Name', 'Dept', 'Course', 'Students'])
            for instructor in self.instructors:
                for course in instructor.students.keys():
                    # add rows according to courses
                    pt.add_row([instructor.cwid, instructor.name, instructor.dept, course, instructor.students[course]])
        else:
            raise ValueError(f'Please enter student or instructor')
        return pt


class Student:
    """
    Student Class
    """

    def __init__(self, cwid):
        # student profile, only needs cwid to be created
        # other attributes may be added later
        self.cwid = cwid
        self.name = ''
        self.major = ''
        self.courses = defaultdict(str)


class Instructor:
    """
    Instructor Class
    """

    def __init__(self, cwid):
        # instructor profile, only needs cwid to be created
        # other attributes may be added later
        self.cwid = cwid
        self.dept = ''
        self.name = ''
        self.students = defaultdict(int)


def main():
    sit = Repository('sit')


if __name__ == '__main__':
    main()
