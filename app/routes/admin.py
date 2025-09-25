from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Report, Message


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(func):
	from functools import wraps
	@wraps(func)
	def wrapper(*args, **kwargs):
		if not current_user.is_authenticated or not current_user.is_admin:
			flash("Admin access required.", "warning")
			return redirect(url_for("auth.login"))
		return func(*args, **kwargs)
	return wrapper


@admin_bp.route("/reports")
@login_required
@admin_required
def reports():
	reports = Report.query.order_by(Report.created_at.desc()).all()
	return render_template("admin/reports.html", reports=reports)


@admin_bp.route("/reports/delete/<int:message_id>")
@login_required
@admin_required
def delete_message(message_id: int):
	message = Message.query.get_or_404(message_id)
	db.session.delete(message)
	db.session.commit()
	flash("Message deleted.", "success")
	return redirect(url_for("admin.reports"))
