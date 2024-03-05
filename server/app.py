from http.client import BAD_REQUEST
from flask import Flask, make_response, request, jsonify, abort, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, User, Parcel, Delivery, Location, UserNotification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SendIT.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api= Api(app)


@app.errorhandler(NotFound)
def handle_not_found(e):
    return render_template('index.html', title='Homepage', message='Welcome to our website!')

class UsersList(Resource):
    def get(self):
        users = User.query.all()
        return [{"id": user.id, "username": user.username, "email":user.email} for user in users] 

    def post(self):
        data = request.get_json()
        username = data['username']
        email =data ['email']
        password = data['password']
        

        if not username:
            abort(400, description="Username is required.")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            abort(400, description="User with this username already exists.")

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        response = make_response(jsonify(new_user.serialize()), 201)
        return response

api.add_resource(UsersList, "/users")


if __name__ == '__main__':
    app.run(port=5555, debug=True)