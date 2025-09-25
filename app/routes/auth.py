from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..forms import RegistrationForm, LoginForm
from ..models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("main.chat"))
	form = RegistrationForm()
	if form.validate_on_submit():
		if User.query.filter_by(email=form.email.data.lower()).first():
			flash("Email is already registered.", "warning")
			return redirect(url_for("auth.register"))
		user = User(email=form.email.data.lower())
		user.password = form.password.data
		db.session.add(user)
		db.session.commit()
		flash("Registration successful. You can now log in.", "success")
		return redirect(url_for("auth.login"))
	return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main.chat"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if not user or not user.verify_password(form.password.data):
			flash("Invalid email or password.", "danger")
			return redirect(url_for("auth.login"))
		login_user(user, remember=form.remember.data)
		flash("Logged in successfully.", "success")
		next_page = request.args.get("next") or url_for("main.chat")
		return redirect(next_page)
	return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
	logout_user()
	flash("You have been logged out.", "info")
	return redirect(url_for("auth.login"))
