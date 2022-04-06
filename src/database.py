from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self) -> str:
        return 'User>>> {self.username}'
