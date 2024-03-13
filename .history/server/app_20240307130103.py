from flask import Flask, make_response, request, jsonify, abort
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
    return jsonify({"message": "Resource not found"}), 404


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
        delivery = Delivery.query.get_or_404(delivery_id)
        db.session.delete(delivery)
        db.session.commit()
        return '', 204


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
        location = Location.query.get_or_404(location_id)
        return location.serialize()

    def patch(self, location_id):
        data = request.get_json()
        location = Location.query.get_or_404(location_id)

        if 'location' in data:
            location.location = data['location']
        if 'status' in data:
            location.status = data['status']

        db.session.commit()
        return location.serialize()

    def delete(self, location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return '', 204


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
        notification = UserNotification.query.get_or_404(notification_id)
        return notification.serialize()

    def patch(self, notification_id):
        data = request.get_json()
        notification = UserNotification.query.get_or_404(notification_id)

        if 'notification' in data:
            notification.notification = data['notification']

        db.session.commit()
        return notification.serialize()

    def delete(self, notification_id):
        notification = UserNotification.query.get_or_404(notification_id)
        db.session.delete(notification)
        db.session.commit()
        return '', 204


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


<<<<<<< HEAD
# Add routes for managing parcels, deliveries, locations, and user notifications
api.add_resource(ParcelResource, "/parcels/<int:parcel_id>")
api.add_resource(ParcelsList, "/parcels")
api.add_resource(DeliveryResource, "/deliveries/<int:delivery_id>")
api.add_resource(DeliveriesList, "/deliveries")
api.add_resource(LocationResource, "/locations/<int:location_id>")
api.add_resource(LocationsList, "/locations")
api.add_resource(UserNotificationResource, "/user_notifications/<int:notification_id>")
api.add_resource(UserNotificationsList, "/user_notifications")
=======
class UsersByID(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return {"id": user.id, "username": user.username, "email":user.email}
        else:
            raise NotFound("User not found")
        
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error':'User does not exist'},404
        else:
            db.session.delete(user)
            db.session.commit()
            response = make_response(jsonify({'Message':'User deleted'}), 200)
            return response
    
    def patch(self, user_id):

        existing_user = User.query.get(user_id)
        if not existing_user:
            return {'error':'User does not exist'},404
        
        data = request.get_json()
        if 'username' in data:
            existing_user.username = data['username']
        elif 'email' in data:
            existing_user.email = data['email']
        else:
            return {'error':'No field to update provided'},400

        db.session.commit()

        response = make_response(jsonify(existing_user.serialize()), 200)
        return response

api.add_resource(UsersByID, "/users/<int:user_id>")

>>>>>>> 1f1414129b417b81222cdee9412dd1b4fcc3e7ef

if __name__ == '__main__':
    app.run(port=5555, debug=True)
