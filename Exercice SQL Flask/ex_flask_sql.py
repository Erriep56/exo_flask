from ..app import app, db

followers = db.Table(
    "followers",
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


skills = db.Table(
    "skills",
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('competence_id', db.Integer, db.ForeignKey('competences.competences_id'))
)

message = db.Table(
    "message",
    db.Column('message_expediteur_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_destinataire_id', db.Integer, db.ForeignKey('user.id'))
)


# table User
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(45), nullable=False, unique=True)
    user_firstname = db.Column(db.String(45))
    user_surname = db.Column(db.String(45))
    user_mail = db.Column(db.Text, nullable=False, unique=True)
    user_password_hash = db.Column(db.Text, nullable=False)
    user_birthyear = db.Column(db.Integer)
    user_promotion_date = db.Column(db.String(45))
    user_description = db.Column(db.Text)
    user_last_seen = db.Column(db.DateTime)
    user_linkedin = db.Column(db.Text)
    user_github = db.Column(db.Text)
    user_inscription_date = db.Column(db.DateTime)

    # relations
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user_comment', lazy=True)
    cv = db.relationship('CV', backref='cv')

    following = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('following', lazy='dynamic'), lazy='dynamic'
    )
    messages = db.relationship(
        'User',
        secondary=message,
        primaryjoin=(message.c.message_expediteur_id == id),
        secondaryjoin=(message.c.message_destinataire_id == id),
        backref=db.backref('messages_received', lazy='dynamic'), lazy='dynamic'
        )


    competences = db.relationship(
        'Competences', 
        secondary=skills,
        backref='competences'
    ) 

    def __repr__(self):
        return '<User %r>' % (self.user_name)

# table Post
class Post(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True)
    post_titre = db.Column(db.String(45))
    post_message = db.Column(db.Text)
    post_date = db.Column(db.DateTime)
    post_indexation = db.Column(db.String(45))
    html = db.Column(db.Text)

    post_auteur = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    def __repr__(self):
        return '<Post %r>' % (self.post_titre)

# table Commentaire
class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    comment_message = db.Column(db.Text)
    comment_html = db.Column(db.Text)
    comment_date = db.Column(db.DateTime)
    
    comment_post = db.Column(
        db.Integer, 
        db.ForeignKey('post.post_id')
    )
    comment_auteur = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )

    # db.relationships
    post = db.relationship(
        'Post', 
        backref='post_comments',
        lazy=True
    )

    def __repr__(self):
        return '<comment %r>' % (self.comment_message)


# table Message
class Message(db.Model):
    __tablename__ = 'message'

    message_id = db.Column(db.Integer, primary_key=True)
    message_message = db.Column(db.Text)
    message_html = db.Column(db.Text)
    message_date = db.Column(db.DateTime)
    message_expediteur_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id')
    )

    message_destinataire_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id')
    )

    def __repr__(self):
        return '<Message %r>' % (self.message_message)

# table cv
class CV(db.Model):
    __tablename__ = 'cv'

    cv_id = db.Column(db.Integer, primary_key=True)
    cv_nom_poste = db.Column(db.Text)
    cv_nom_employeur = db.Column(db.Text)
    cv_ville = db.Column(db.String(45))
    cv_annee_debut = db.Column(db.Integer)
    cv_annee_fin = db.Column(db.Integer)
    cv_description_poste = db.Column(db.Text)
    
    cv_utilisateur = db.Column(
        db.Integer, 
        db.ForeignKey('user.id')
    )

    # db.relationships
    user = db.relationship('User', backref='cvs')

    def __repr__(self):
        return '<CV %r>' % (self.cv_nom_poste)

# table competences
class Competences(db.Model):
    __tablename__ = 'competences'

    competences_id = db.Column(db.Integer, primary_key=True)
    competences_label = db.Column(db.String(45))

    def __repr__(self):
        return '<Competences %r>' % (self.competences_label)