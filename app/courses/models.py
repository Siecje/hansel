from flask import current_app, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.core import db


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    students = db.relationship('User', backref='course', lazy='dynamic')
    assignments = db.relationship('Assignment', backref='course', lazy='dynamic')

    def __repr__(self):
        return '<Course %r>' % self.name


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

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
