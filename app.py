# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = True
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

db = SQLAlchemy(app)
api = Api(app)

ns_movies = api.namespace("movies")
ns_genre = api.namespace("genres")
ns_director = api.namespace("directors")

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Director_Schema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


@ns_movies.route("/")
class MovieView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        page = request.args.get("page")
        movies = Movie.query
        try:
            if director_id:
                movies = movies.filter(Movie.director_id == director_id)
            if genre_id:
                movies = movies.filter(Movie.genre_id == genre_id)
            movies = movies.all()
            return MovieSchema(many=True).dump(movies), 200
        except Exception as e:
            return str(e), 404


    def post(self):
        data = request.get_json()
        # movie = Movie.query.filter(Movie.title == data["title"], Movie.year == data["year"])
        # if len(movie) > 0:
        #     return "Запись уже есть!", 400

        new_movie = Movie(**data)
        db.session.add(new_movie)
        db.session.commit()
        db.session.close()
        return "", 201





@ns_movies.route("/<int:m_id>")
class MovieView(Resource):
    def get(self, m_id):
        try:
            movie = Movie.query.get(m_id)
            return MovieSchema().dump(movie), 200
        except Exception as e:
            return str(e), 404


    def put(self, m_id):
        data = request.get_json()
        movie = Movie.query.get(m_id)

        movie.id = data["id"]
        movie.title = data["title"]
        movie.description = data["description"]
        movie.trailer = data["trailer"]
        movie.year = data["year"]
        movie.rating = data["rating"]
        movie.genre_id = data["genre_id"]
        movie.director_id = data["director_id"]

        db.session.add(movie)
        db.session.commit()
        db.session.close()

        return "", 204


    def patch(self, m_id):
        data = request.get_json()
        movie = Movie.query.get(m_id)
        if "id" in data:
            movie.id = data["id"]
        if "title" in data:
            movie.title = data["title"]
        if "description" in data:
            movie.description = data["description"]
        if "trailer" in data:
            movie.trailer = data["trailer"]
        if "year" in data:
            movie.year = data["year"]
        if "rating" in data:
            movie.rating = data["rating"]
        if "genre_id" in data:
            movie.genre_id = data["genre_id"]
        if "director_id" in data:
            movie.director_id = data["director_id"]

        db.session.add(movie)
        db.session.commit()
        db.session.close()

        return "", 204


    def delete(self, m_id):
        movie = Movie.query.get(m_id)
        db.session.delete(movie)
        db.session.commit()
        db.session.close()

        return "", 204


@ns_genre.route("/")
class GenreView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()

        return GenreSchema(many=True).dump(genres), 200


    def post(self):
        data = request.get_json()
        new_genre = Genre(**data)

        db.session.add(new_genre)
        db.session.commit()
        db.session.close()

        return "", 201


@ns_genre.route("/<int:g_id>")
class GenreView(Resource):
    def get(self, g_id):
        genre = db.session.query(Genre).get(g_id)
        return GenreSchema().dump(genre), 200


    def put(self, g_id):
        data = request.get_json()
        genre = Genre.query.get(g_id)

        genre.id = data["id"]
        genre.name = data["name"]

        db.session.add(genre)
        db.session.commit()
        db.session.close()

        return "", 204


    def patch(self, g_id):
        data = request.get_json()
        genre = Genre.query.get(g_id)
        if "id" in data:
            genre.id = data["id"]
        if "name" in data:
            genre.name = data["name"]
        db.session.add(genre)
        db.session.commit()
        db.session.close()

        return "", 204


    def delete(self, g_id):
        genre = Genre.query.get(g_id)

        db.session.delete(genre)
        db.session.commit()
        db.session.close()

@ns_director.route("/")
class DirectorView(Resource):
    def get(self):
        directors = Director.query.all()
        return Director_Schema(many=True).dump(directors), 200


    def post(self):
        data = request.get_json()
        new_director = Director(**data)

        db.session.add(new_director)
        db.session.commit()
        db.session.close()

        return "", 201


@ns_director.route("/<int:d_id>")
class DirectorView(Resource):
    def get(self, d_id):
        director = Director.query.get(d_id)
        return Director_Schema().dump(director), 200


    def put(self, d_id):
        data = request.get_json()
        director = Director.query.get(d_id)
        director.id = data["id"]
        director.name = data["name"]

        db.session.add(director)
        db.session.commit()
        db.session.close()

        return "", 204


    def patch(self, d_id):
        data = request.get_json()
        director = Director.query.get(d_id)
        if "id" in data:
            director.id = data["id"]
        if "name" in data:
            director.name = data["name"]

        db.session.add(director)
        db.session.commit()
        db.session.close()

        return "", 204


    def delete(self, d_id):
        director = Director.query.get(d_id)
        db.session.delete(director)
        db.session.commit()
        db.session.close()

        return "", 204


if __name__ == '__main__':
    app.run()
