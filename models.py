# import cryptacular.bcrypt
import hashlib

from sqlalchemy import (
	Table,
	Column,
	ForeignKey,
	)

from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
	relation,
	column_property,
	synonym,
	joinedload,
	)

from sqlalchemy.types import (
	Integer,
	Unicode,
	UnicodeText,
	)

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
	Everyone,
	Authenticated,
	Allow,
	)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

hash5 = hashlib.md5()

# crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def hash_password(password):
	hash5.update(password)
	return hash5.hexdigest()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(Unicode(30), unique=True)
    name = Column(Unicode(50))
    email = Column(Unicode(50))

    _password = Column('password', Unicode(60))

    def _get_password(self):
    	return self._password

	def _set_password(self, password):
		self._password = hash_password(password)

	password = property(_get_password, _set_password)
	password = synonym('_password', descriptor=password)

	def __init__(self, username, password, name, email):
		self.username = username
		self.name = name
		self.email = email
		self.password = password

		@classmethod
		def get_by_username(cls, username):
			return DBSession.query(cls).filter(cls.username == username).first()

		@classmethod
		def check_password(cls, username, password):
			user = cls.get_by_username(username)
			if not user:
				return False
			return crypt.check(user.password, password)


class Ticket(Base):
	__tablename__ = 'tickets'
	ticket_id = Column(Integer, primary_key=True)
	title = Column(UnicodeText, unique=True)
	content = Column(UnicodeText)
	author_id = Column(Integer, ForeignKey('users.user_id'))
	author = relation(User, cascade="delete", backref='tickets')
	status = Column(Integer, default=0)


class RootFactory(object):
	__acl__ = [
		(Allow, Everyone, 'view'),
		(Allow, Authenticated, 'post')
	]

	def __init__(self, request):
		pass


