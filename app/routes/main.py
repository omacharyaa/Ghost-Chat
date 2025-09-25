from __future__ import annotations

import random
from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user

from ..regions import COUNTRIES, INDIA_CITIES
from ..models import Group


main_bp = Blueprint("main", __name__)

ROOMS = ["General", "Sports", "Tech", "Love", "Dating"]


@main_bp.route("/")
def index():
	return redirect(url_for("main.chat"))


@main_bp.route("/about")
def about():
	return render_template("about.html")


@main_bp.route("/toggle-theme", methods=["POST"]) 
def toggle_theme():
	current = session.get("theme", "light")
	session["theme"] = "dark" if current == "light" else "light"
	return redirect(request.referrer or url_for("main.chat"))


@main_bp.route("/nickname", methods=["POST"]) 
@login_required
def set_nickname():
	new_name = (request.form.get("nickname") or "").strip()
	if new_name:
		session["nickname"] = new_name
	return redirect(request.referrer or url_for("main.chat"))


@main_bp.route("/region", methods=["GET", "POST"])
def region():
	if request.method == "POST":
		country = request.form.get("country") or "Global"
		city = request.form.get("city")
		custom = request.form.get("custom")
		if country == "India" and city:
			region_value = f"India - {city}"
		elif custom:
			region_value = custom.strip()
		else:
			region_value = country
		session["region"] = region_value or "Global"
		return redirect(url_for("main.chat"))
	return render_template("region.html", countries=COUNTRIES, india_cities=INDIA_CITIES)


@main_bp.route("/chat")
@login_required
def chat():
	region = session.get("region", "Global")
	nickname = session.get("nickname")
	if not nickname:
		nickname = f"Ghost-{random.randint(1000, 9999)}"
		session["nickname"] = nickname
	group_code = session.get("group_code")
	group_name = None
	if group_code:
		g = Group.query.filter_by(code=group_code).first()
		if g:
			group_name = g.name
	return render_template("chat.html", rooms=ROOMS, region=region, nickname=nickname, group_code=group_code, group_name=group_name)
