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

api = Api(app)


@app.errorhandler(NotFound)
def handle_not_found(e):
    return render_template('index.html', title='Homepage', message='Welcome to SendIT')


class UsersList(Resource):
    def get(self):
        users = User.query.all()
        return [{"id": user.id, "username": user.username, "email": user.email} for user in users]

    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            abort(400, description="Username, email, and password are required.")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            abort(400, description="User with this username already exists.")

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        response = make_response(jsonify(new_user.serialize()), 201)
        return response
class ParcelsList(Resource):
    def get(self):
        parcels = Parcel.query.all()
        return [parcel.serialize() for parcel in parcels]

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        weight = data.get('weight')
        status = data.get('status')

        if not all([user_id, weight, status]):
            abort(400, description="User ID, weight, and status are required.")

        parcel = Parcel(user_id=user_id, weight=weight, status=status)
        db.session.add(parcel)
        db.session.commit()

        response = make_response(jsonify(parcel.serialize()), 201)
        return response

class DeliveriesList(Resource):
    def get(self):
        deliveries = Delivery.query.all()
        return [delivery.serialize() for delivery in deliveries]

    def post(self):
        data = request.get_json()
        parcel_id = data.get('parcel_id')
        title = data.get('title')
        body = data.get('body')
        status = data.get('status')

        if not all([parcel_id, title, body, status]):
            abort(400, description="Parcel ID, title, body, and status are required.")

        delivery = Delivery(parcel_id=parcel_id, title=title, body=body, status=status)
        db.session.add(delivery)
        db.session.commit()

        response = make_response(jsonify(delivery.serialize()), 201)
        return response

class LocationsList(Resource):
    def get(self):
        locations = Location.query.all()
        return [location.serialize() for location in locations]

    def post(self):
        data = request.get_json()
        delivery_id = data.get('delivery_id')
        location = data.get('location')
        status = data.get('status')

        if not all([delivery_id, location, status]):
            abort(400, description="Delivery ID, location, and status are required.")

        location = Location(delivery_id=delivery_id, location=location, status=status)
        db.session.add(location)
        db.session.commit()

        response = make_response(jsonify(location.serialize()), 201)
        return response

class UserNotificationsList(Resource):
    def get(self):
        notifications = UserNotification.query.all()
        return [notification.serialize() for notification in notifications]

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        notification = data.get('notification')
        delivery_id = data.get('delivery_id')

        if not all([user_id, notification, delivery_id]):
            abort(400, description="User ID, notification, and delivery ID are required.")

        notification = UserNotification(user_id=user_id, notification=notification, delivery_id=delivery_id)
        db.session.add(notification)
        db.session.commit()

        response = make_response(jsonify(notification.serialize()), 201)
        return response


# Add routes for managing parcels, deliveries, locations, and user notifications
api.add_resource(LocationResource, "/locations/int:location_id")
api.add_resource(LocationsList, "/locations")
api.add_resource(UserNotificationResource, "/user_notifications/int:notification_id")
api.add_resource(UserNotificationsList, "/user_notifications")
api.add_resource(UsersList, "/users")

if __name__ == '__main__':
    app.run(port=5555, debug=True)