from flask import Flask, make_response, request, jsonify, abort, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import  CORS
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from werkzeug.exceptions import NotFound
from models import db, User, Parcel, Delivery, Location, UserNotification
from auth import auth_bp
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = b'\xb2\xd3B\xb9 \xab\xc0By\x13\x10\x84\xb7M!\x11'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SendIT.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)
CORS(app)
jwt = JWTManager()
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

# @app.errorhandler(NotFound)
# def handle_not_found(e):
#     return render_template('index.html', title='Homepage', message='Welcome to SendIT')


class ParcelResource(Resource):
    def get(self, parcel_id):
        parcel = Parcel.query.get_or_404(parcel_id)
        return parcel.serialize()

    def patch(self, parcel_id):
        data = request.get_json()
        parcel = Parcel.query.get_or_404(parcel_id)

        if 'weight' in data:
            parcel.weight = data['weight']
        if 'status' in data:
            parcel.status = data['status']

        db.session.commit()
        return parcel.serialize()

    def delete(self, parcel_id):
        parcel = Parcel.query.get_or_404(parcel_id)
        db.session.delete(parcel)
        db.session.commit()
        return '', 204


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


class DeliveryResource(Resource):
    def get(self, delivery_id):
        delivery = Delivery.query.get_or_404(delivery_id)
        return delivery.serialize()

    def patch(self, delivery_id):
        data = request.get_json()
        delivery = Delivery.query.get_or_404(delivery_id)

        if 'title' in data:
            delivery.title = data['title']
        if 'body' in data:
            delivery.body = data['body']
        if 'status' in data:
            delivery.status = data['status']

        db.session.commit()
        return delivery.serialize()

    def delete(self, delivery_id):
        delivery = Delivery.query.get(delivery_id)
        if not delivery :
            return {'error':'Delivery does not exist'},404
        else :
            db.session.delete(delivery)
            db.session.commit()
            response = make_response(jsonify({'Message':'Delivery deleted'}), 200)
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


class LocationResource(Resource):
    def get(self, location_id):
        location = Location.query.get(location_id)
        if location:
            return {"id":location.id,"delivery_id":location.delivery_id,"location":location.location, "status":location.status}
        else:
            raise NotFound("Location not found")

    def patch(self, location_id):
        existing_location = Location.query.get(location_id)
        if not existing_location:
            return {'error':'Location does not exist'},404
        data = request.get_json()
        location = Location.query.get_or_404(location_id)

        if 'location' in data:
            location.location = data['location']
        if 'status' in data:
            location.status = data['status']

        db.session.commit()
        return location.serialize()

    def delete(self, location_id):
        location = Location.query.get(location_id)
        if location is None :
            return{"error":"This delivery location does not exist"},404
        else:
            db.session.delete(location)
            db.session.commit()
            response =make_response(jsonify({"message":"Location successfully deleted"}), 200)
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


class UserNotificationResource(Resource):
    def get(self, notification_id):
        notification = UserNotification.query.get(notification_id)
        if notification is None:
            abort(404, "Notification id '{}' does not exist.".format(notification_id))
        return notification.serialize()

    def patch(self, notification_id):
        existing_notification = UserNotification.query.get(notification_id)
        if not existing_notification:
            return {'error':'Notification does not exist'},404
        data = request.get_json()
        if 'notification' in data:
            existing_notification.notification = data['notification']
        else:
            return {'error':'No field to update provided'},400

        db.session.commit()
        response = make_response(jsonify(existing_notification.serialize()), 200)
        return response

    def delete(self, notification_id):
        notification = UserNotification.query.get(notification_id)
        if notification is None:
            return {"error": "Notification does not exist."}, 404
        else:
            db.session.delete(notification)
            db.session.commit()
            response =make_response(jsonify({"message":"Notification successfully deleted"}), 200)
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
api.add_resource(ParcelResource, "/parcels/<int:parcel_id>")
api.add_resource(ParcelsList, "/parcels")
api.add_resource(DeliveryResource, "/deliveries/<int:delivery_id>")
api.add_resource(DeliveriesList, "/deliveries")
api.add_resource(LocationResource, "/locations/<int:location_id>")
api.add_resource(LocationsList, "/locations")
api.add_resource(UserNotificationResource, "/notifications/<int:notification_id>")
api.add_resource(UserNotificationsList, "/notifications")



if __name__ == '__main__':
    app.run(port=5555, debug=True)
