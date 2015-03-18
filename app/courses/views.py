from werkzeug import secure_filename
from flask import abort, render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import current_user, login_required
from app.core import db
from . import courses
from .models import Course, Assignment, Submission
from .forms import CourseForm, AssignmentForm, SubmissionForm


@courses.route('/courses/create', methods=['GET', 'POST'])
@login_required
def create_course():
    if current_user.role.name != 'Instructor':
        abort(404)

    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data,
                        instructor=current_user)

        db.session.add(course)
        db.session.commit()
        return redirect(url_for('courses.view_course', id=course.id))
    return render_template('courses/create.html', form=form)


@courses.route('/courses/<id>', methods=['GET', 'POST'])
@login_required
def view_course(id):
    course = Course.query.get_or_404(id)
    if course not in current_user.courses and course not in current_user.created_courses:
        abort(404)
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(name=form.name.data,
                                course=course)
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for('courses.view_course', id=course.id))
    return render_template('courses/view.html', course=course, form=form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@courses.route('/courses/<course_id>/<assignment_id>', methods=['GET', 'POST'])
@login_required
def view_assignment(course_id, assignment_id):
    course = Course.query.get_or_404(course_id)
    if course not in current_user.courses and course not in current_user.created_courses:
        abort(404)
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment not in course.assignments:
        abort(404)
    form = SubmissionForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(current_app.config['SUBMISSION_FOLDER'] + filename)
        submission = Submission(file_name=filename, assignment=assignment, student=current_user)
        db.session.add(submission)
        flash('Submission Uploaded')
        return redirect(url_for('courses.view_assignment', course_id=course.id, assignment_id=assignment.id))
    return render_template('courses/view_assignment.html', course=course, assignment=assignment, form=form)


@courses.route('/courses/<course_id>/<assignment_id>/<submission_id>')
@login_required
def view_submission(course_id, assignment_id, submission_id):
    course = Course.query.get_or_404(course_id)
    if course not in current_user.courses and course not in current_user.created_courses:
        abort(404)
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment not in course.assignments:
        abort(404)
    submission = Submission.query.get_or_404(submission_id)
    if submission not in assignment.submissions:
        abort(404)
    return render_template('courses/view_submission.html', course=course, assignment=assignment, submission=submission)
