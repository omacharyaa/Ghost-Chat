from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Profile
from ..forms import ProfileForm


profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/me", methods=["GET", "POST"])
@login_required
def me():
	profile = current_user.profile or Profile(user_id=current_user.id)
	form = ProfileForm(obj=profile)
	if form.validate_on_submit():
		profile.name = (form.name.data or "").strip() or None
		profile.gender = form.gender.data or None
		profile.age = form.age.data
		profile.height_cm = form.height_cm.data
		profile.interests = (form.interests.data or "").strip() or None
		if profile.id is None:
			db.session.add(profile)
		db.session.commit()
		flash("Profile updated.", "success")
		next_url = request.form.get("next")
		if next_url and url_for("profile.me") not in next_url:
			return redirect(next_url)
		return redirect(url_for("main.chat"))
	# GET request
	next_url = request.args.get("next") or request.referrer or url_for("main.chat")
	return render_template("profile/edit.html", form=form, profile=profile, next_url=next_url)


@profile_bp.route("/<int:user_id>")
@login_required
def view(user_id: int):
	profile = Profile.query.filter_by(user_id=user_id).first()
	return render_template("profile/view.html", profile=profile)
