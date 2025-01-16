from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for the skills relationship
class Skill(Base):
    __tablename__ = 'skills'
    user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
    competence_id = Column(Integer, ForeignKey('Competences.competences_id'), primary_key=True)

# User table
class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(45), nullable=False)
    user_firstname = Column(String(45), nullable=False)
    user_surname = Column(String(45), nullable=False)
    user_mail = Column(String(45), unique=True, nullable=False)
    user_password_hash = Column(Text, nullable=False)
    user_birthyear = Column(Integer)
    user_promotion_date = Column(String(45))
    user_description = Column(Text)
    user_last_seen = Column(DateTime)
    user_linkedin = Column(Text)
    user_github = Column(Text)
    user_inscription_date = Column(DateTime, nullable=False)

    # Relationships
    posts = relationship('Post', back_populates='author', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='author', cascade='all, delete-orphan')
    messages_sent = relationship('Message', foreign_keys='Message.message_expediteur_id', back_populates='sender', cascade='all, delete-orphan')
    messages_received = relationship('Message', foreign_keys='Message.message_destinataire_id', back_populates='recipient', cascade='all, delete-orphan')
    followers = relationship('Follower', foreign_keys='Follower.followed_id', back_populates='followed', cascade='all, delete-orphan')
    following = relationship('Follower', foreign_keys='Follower.follower_id', back_populates='follower', cascade='all, delete-orphan')
    skills = relationship('Competence', secondary='skills', back_populates='users')
    cvs = relationship('CV', back_populates='user', cascade='all, delete-orphan')

# Follower table
class Follower(Base):
    __tablename__ = 'followers'

    follower_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('User.id'), primary_key=True)

    # Relationships
    follower = relationship('User', foreign_keys=[follower_id], back_populates='following')
    followed = relationship('User', foreign_keys=[followed_id], back_populates='followers')

# Post table
class Post(Base):
    __tablename__ = 'Post'

    post_id = Column(Integer, primary_key=True)
    post_titre = Column(String(45), nullable=False)
    post_message = Column(Text, nullable=False)
    post_date = Column(DateTime, nullable=False)
    post_indexation = Column(String(45))
    html = Column(Text)
    post_auteur = Column(Integer, ForeignKey('User.id'), nullable=False)

    # Relationships
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')

# Comment table
class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True)
    comment_message = Column(Text, nullable=False)
    comment_html = Column(Text)
    comment_date = Column(DateTime, nullable=False)
    comment_post = Column(Integer, ForeignKey('Post.post_id'), nullable=False)
    comment_auteur = Column(Integer, ForeignKey('User.id'), nullable=False)

    # Relationships
    post = relationship('Post', back_populates='comments')
    author = relationship('User', back_populates='comments')

# Message table
class Message(Base):
    __tablename__ = 'Message'

    message_id = Column(Integer, primary_key=True)
    message_message = Column(Text, nullable=False)
    message_html = Column(Text)
    message_date = Column(DateTime, nullable=False)
    message_expediteur_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    message_destinataire_id = Column(Integer, ForeignKey('User.id'), nullable=False)

    # Relationships
    sender = relationship('User', foreign_keys=[message_expediteur_id], back_populates='messages_sent')
    recipient = relationship('User', foreign_keys=[message_destinataire_id], back_populates='messages_received')

# CV table
class CV(Base):
    __tablename__ = 'CV'

    cv_id = Column(Integer, primary_key=True)
    cv_nom_poste = Column(Text, nullable=False)
    cv_nom_employeur = Column(Text, nullable=False)
    cv_ville = Column(String(45))
    cv_annee_debut = Column(Integer, nullable=False)
    cv_annee_fin = Column(Integer)
    cv_description_poste = Column(Text)
    cv_utilisateur = Column(Integer, ForeignKey('User.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='cvs')

# Competences table
class Competence(Base):
    __tablename__ = 'Competences'

    competences_id = Column(Integer, primary_key=True)
    competences_label = Column(String(45), nullable=False)

    # Relationships
    users = relationship('User', secondary='skills', back_populates='skills')

