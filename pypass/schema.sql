-- not really needed because sqlalchemy is used

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  social_id text not null,
  nickname text not null,
  email text not null
);

--id = db.Column(db.Integer, primary_key=True)
--username = db.Column(db.String(64), nullable=False, unique=True)
--social_id = db.Column(db.String(64), nullable=False, unique=True)
--nickname = db.Column(db.String(64), nullable=False)
--email = db.Column(db.String(64), nullable=True)