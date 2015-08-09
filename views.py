import formencode

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render, render_to_response
# from pyramid.renderers import render

from pyramid.security import (
	authenticated_userid,
	remember,
	forget,
	)

from models import (
	DBSession,
	User,
	Ticket
	)

@view_config(permission='view', route_name='main',
	renderer='templates/main.pt', request_method='GET')
def main_view(request):
	login_form = login_form_view(request)

	return render_to_response( 'templates/main.pt', {} )
	#	return Response('hello')
	#return {
	#	'login_form': 'render',
	#}

def login_form_view(request):
	logged_in = authenticated_userid(request)
	return render('templates/login.pt', {'loggedin': logged_in}, request)

