from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user


auth=Blueprint('auth', __name__)


@auth.route('/')
def login():
    return 'login'