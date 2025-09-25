from __future__ import annotations

import re
from typing import Iterable

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, NumberRange, Optional


PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$")


def validate_strong_password(form: FlaskForm, field: PasswordField) -> None:
	value = field.data or ""
	if not PASSWORD_REGEX.match(value):
		raise ValidationError(
			"Password must be 8+ chars with uppercase, lowercase, number, and special character."
		)


class RegistrationForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
	password = PasswordField("Password", validators=[DataRequired(), validate_strong_password])
	agree = BooleanField("Agree to rules", validators=[DataRequired()])
	submit = SubmitField("Create account")


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember me")
	submit = SubmitField("Log in")


class ReportForm(FlaskForm):
	reason = StringField("Reason", validators=[DataRequired(), Length(max=255)])
	submit = SubmitField("Report")


class ProfileForm(FlaskForm):
	name = StringField("Name", validators=[Optional(), Length(max=80)])
	gender = SelectField(
		"Gender",
		choices=[("", "Prefer not to say"), ("male", "Male"), ("female", "Female"), ("other", "Other")],
		validators=[Optional()],
	)
	age = IntegerField("Age", validators=[Optional(), NumberRange(min=13, max=120)])
	height_cm = IntegerField("Height (cm)", validators=[Optional(), NumberRange(min=50, max=300)])
	interests = TextAreaField("Interests", validators=[Optional(), Length(max=500)])
	submit = SubmitField("Save profile")
