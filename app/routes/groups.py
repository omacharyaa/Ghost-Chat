from __future__ import annotations

from flask import Blueprint, request, redirect, url_for, flash, session
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Group


groups_bp = Blueprint("groups", __name__, url_prefix="/groups")


@groups_bp.route("/create", methods=["POST"])
@login_required
def create_group():
	name = (request.form.get("name") or "").strip()
	if not name:
		flash("Group name is required.", "warning")
		return redirect(url_for("main.chat"))
	region = session.get("region")
	group = Group.create_unique(name=name, region=region, created_by=current_user.id)
	db.session.add(group)
	db.session.commit()
	session["group_code"] = group.code
	flash(f"Group '{group.name}' created. Code: {group.code}", "success")
	return redirect(url_for("main.chat"))


@groups_bp.route("/join", methods=["POST"])
@login_required
def join_group():
	code = (request.form.get("code") or "").strip().upper()
	if not code:
		flash("Room code is required.", "warning")
		return redirect(url_for("main.chat"))
	group = Group.query.filter_by(code=code).first()
	if not group:
		flash("Invalid room code.", "danger")
		return redirect(url_for("main.chat"))
	session["group_code"] = group.code
	session["region"] = group.region or session.get("region", "Global")
	flash(f"Joined group '{group.name}'.", "success")
	return redirect(url_for("main.chat"))


@groups_bp.route("/leave", methods=["POST"])
@login_required
def leave_group():
	session.pop("group_code", None)
	flash("Left group.", "info")
	return redirect(url_for("main.chat"))
