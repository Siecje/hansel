from flask import abort, render_template, redirect, request, url_for, flash
from flask.ext.login import current_user
from app.core import db
from . import courses
from .models import Course, Assignment
from .forms import CourseForm, AssignmentForm


@courses.route('/courses/create', methods=['GET', 'POST'])
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data,
                        instructor=current_user)

        db.session.add(course)
        db.session.commit()
        return redirect(url_for('courses.view_course', id=course.id))
    return render_template('courses/create.html', form=form)


@courses.route('/courses/<id>', methods=['GET', 'POST'])
def view_course(id):
    course = Course.query.get_or_404(id)
    if course not in current_user.courses:
        abort(404)
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(name=form.name.data,
                                course=course)
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('courses.view_course', id=course.id))
    return render_template('courses/view.html', course=course, form=form)


@courses.route('/courses/<course_id>/<assignment_id>', methods=['GET'])
def view_assignment(course_id, assignment_id):
    course = Course.query.get_or_404(course_id)
    if course not in current_user.courses:
        abort(404)
    assignment = Assignment.query.get_or_404(assignment_id)
    return render_template('courses/view_assignment.html', course=course, assignment=assignment)


@courses.route('/courses/<course_id>/<assignment_id>/<submission_id>')
def view_submission(course_id, assignment_id, submission_id):
    course = Course.query.get_or_404(course_id)
    if course not in current_user.courses:
        abort(404)
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment not in course.assignments:
        abort(404)
    submission = Submission.query.get_or_404(submission_id)
    if submission not in assignment.submissions:
        abort(404)
    return render_template('courses/view_submission.html', course=course, assignment=assignment, submission=submission)
