"""
SSW810-HW12_Yuning_Sun by Yuning Sun
5:02 下午 11/19/19
Module documentation: 
"""
import sqlite3

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/instructors')
def get_instructors():
    # load db path
    db_path = '810_startup.db'
    try:
        db = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        raise sqlite3.OperationalError(f'Can not find table in path {db_path}')
    else:
        # get data
        query = 'select i.CWID, i.Name, i.Dept, g.Course, count(g.StudentCWID) as StudentNum from instructors i left join grades g on i.CWID=g.InstructorCWID group by g.Course, g.InstructorCWID'
        data = [{'cwid': cwid,
                 'name': name,
                 'dept': dept,
                 'course': course,
                 'students': students}
                for cwid, name, dept, course, students in db.execute(query)]
    # return page and params
    return render_template('instructors.html',
                           title='Stevens Repository',
                           table_title='Courses and student counts',
                           instructors=data)


app.run(debug=True)
