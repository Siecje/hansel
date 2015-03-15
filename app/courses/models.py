from flask import current_app, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.core import db


course_users = db.Table('course_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    instructor = db.relationship('User', foreign_keys=[instructor_id], backref=db.backref('created_courses', order_by=id))
    students = db.relationship('User', secondary=course_users, backref=db.backref('courses', lazy='dynamic'))
    assignments = db.relationship('Assignment', backref='course', lazy='dynamic')

    def __repr__(self):
        return '<Course %r>' % self.name


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    def __repr__(self):
        return '<Assignment %r>' % self.name


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))

    def __repr__(self):
        return '<Submission %r>' % self.file_name
