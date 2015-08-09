from pyramid.config import Configurator
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from wsgiref.simple_server import make_server
from sqlalchemy import create_engine

from models import (
	DBSession,
	RootFactory,
	)

#def main(global_config, **settings):
if __name__ == '__main__':
	
	# engine = engine_from_config(settings, 'sqlalchemy.')
	engine = create_engine('mysql://root:@localhost/ticketmid')
	DBSession.configure(bind=engine)

	session_factory = UnencryptedCookieSessionFactoryConfig(
		'alabalanica'
		)

	authn_policy = SessionAuthenticationPolicy()
	authz_policy = ACLAuthorizationPolicy()

	config = Configurator(
		#settings=settings,
		root_factory=RootFactory,
		authentication_policy=authn_policy,
		authorization_policy=authz_policy,
		session_factory=session_factory
		)
	from views import main_view
	config.include('pyramid_chameleon')
#	config.include(addroutes)
	config.add_route('main', '/')
	config.add_view(main_view, route_name='main')
	config.scan()

	app = config.make_wsgi_app()
	server = make_server('0.0.0.0', 8080, app)
	server.serve_forever()
	# return config.make_wsgi_app()

def addroutes(config):
	config.add_route('main', '/main')
