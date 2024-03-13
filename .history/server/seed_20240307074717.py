from models import db, User, Parcel, Delivery, Location, UserNotification

from app  import app

with app.app_context():
    User.query.delete()
    Parcel.query.delete()
    Delivery.query.delete()
    Location.query.delete()
    UserNotification.query.delete()

    # Create users
    users_data = [
        {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'},
        {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
        {'username': 'user3', 'email': 'user3@example.com', 'password': 'password3'},
        {'username': 'user4', 'email': 'user4@example.com', 'password': 'password4'},
        {'username': 'user5', 'email': 'user5@example.com', 'password': 'password5'},
        {'username': 'user6', 'email': 'user6@example.com', 'password': 'password6'},
        {'username': 'user7', 'email': 'user7@example.com', 'password': 'password7'},
        {'username': 'user8', 'email': 'user8@example.com', 'password': 'password8'},
        {'username': 'user9', 'email': 'user9@example.com', 'password': 'password9'},
        {'username': 'user10', 'email': 'user10@example.com', 'password': 'password10'}
    ]

    for data in users_data:
        user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(user)

    db.session.commit()


    # Seed parcels
    parcels_data = [
        {'user_id': 1, 'weight': 10, 'status': 'Pending'},
        {'user_id': 2, 'weight': 15, 'status': 'Delivered'},
        {'user_id': 3, 'weight': 8, 'status': 'Processing'},
        {'user_id': 4, 'weight': 12, 'status': 'Pending'},
        {'user_id': 5, 'weight': 18, 'status': 'Delivered'},
        {'user_id': 6, 'weight': 6, 'status': 'Processing'},
        {'user_id': 7, 'weight': 14, 'status': 'Pending'},
        {'user_id': 8, 'weight': 20, 'status': 'Delivered'},
        {'user_id': 9, 'weight': 9, 'status': 'Processing'},
        {'user_id': 10, 'weight': 11, 'status': 'Pending'}
    ]

    for data in parcels_data:
        parcel = Parcel(user_id=data['user_id'], weight=data['weight'], status=data['status'])
        db.session.add(parcel)

    db.session.commit()

        # Seed deliveries
    deliveries_data = [
        {'parcel_id': 1, 'title': 'Package Out for Delivery', 'body': 'Your package is on its way to your address.', 'status': 'Pending'},
        {'parcel_id': 2, 'title': 'Delivery Successful', 'body': 'Your package has been successfully delivered.', 'status': 'Delivered'},
        {'parcel_id': 3, 'title': 'Delivery Delayed', 'body': 'Due to unexpected circumstances, there is a delay in your delivery.', 'status': 'Processing'},
        {'parcel_id': 4, 'title': 'Delivery Attempt Failed', 'body': 'We attempted delivery but failed to reach you. Please contact us to reschedule.', 'status': 'Pending'},
        {'parcel_id': 5, 'title': 'Delivery in Transit', 'body': 'Your package is currently in transit and will be delivered soon.', 'status': 'Processing'},
        {'parcel_id': 6, 'title': 'Delivery Rescheduled', 'body': 'Your delivery has been rescheduled for a later date.', 'status': 'Pending'},
        {'parcel_id': 7, 'title': 'Delivery Exception', 'body': 'There is an exception with your delivery. Please contact customer support for assistance.', 'status': 'Processing'},
        {'parcel_id': 8, 'title': 'Delivery Received at Sorting Facility', 'body': 'Your package has been received at our sorting facility and will be dispatched shortly.', 'status': 'Pending'},
        {'parcel_id': 9, 'title': 'Delivery Out for Shipment', 'body': 'Your package is out for shipment to its destination.', 'status': 'Processing'},
        {'parcel_id': 10, 'title': 'Delivery Scheduled', 'body': 'Your delivery is scheduled for a specific date and time. Please ensure someone is available to receive it.', 'status': 'Pending'}
    ]

    for data in deliveries_data:
        delivery = Delivery(parcel_id=data['parcel_id'], title=data['title'], body=data['body'], status=data['status'])
        db.session.add(delivery)

    db.session.commit()


    # Seed locations
    locations_data = [
        {'delivery_id': 1, 'location': 'Warehouse A', 'status': 'In Transit'},
        {'delivery_id': 2, 'location': 'Sorting Facility B', 'status': 'In Transit'},
        {'delivery_id': 3, 'location': 'Local Distribution Center', 'status': 'In Transit'},
        {'delivery_id': 4, 'location': 'Delivery Truck En Route', 'status': 'In Transit'},
        {'delivery_id': 5, 'location': 'Out for Delivery', 'status': 'In Transit'},
        {'delivery_id': 6, 'location': 'Sorting Facility C', 'status': 'In Transit'},
        {'delivery_id': 7, 'location': 'Last Mile Delivery Van', 'status': 'In Transit'},
        {'delivery_id': 8, 'location': 'Recipient Address', 'status': 'Out for Delivery'},
        {'delivery_id': 9, 'location': 'Delivery Hub', 'status': 'In Transit'},
        {'delivery_id': 10, 'location': 'Final Destination', 'status': 'Out for Delivery'}
    ]

    for data in locations_data:
        location = Location(delivery_id=data['delivery_id'], location=data['location'], status=data['status'])
        db.session.add(location)

    db.session.commit()

    # Seed user notifications
    notifications_data = [
        {'user_id': 1, 'delivery_id': 1, 'notification': 'Your package is out for delivery.'},
        {'user_id': 2, 'delivery_id': 2, 'notification': 'Your delivery has been delayed.'},
        {'user_id': 3, 'delivery_id': 3, 'notification': 'Your package has arrived at the local distribution center.'},
        {'user_id': 4, 'delivery_id': 4, 'notification': 'Your delivery is on its way to your address.'},
        {'user_id': 5, 'delivery_id': 5, 'notification': 'Your package has been successfully delivered.'},
        {'user_id': 6, 'delivery_id': 6, 'notification': 'Your delivery is in transit.'},
        {'user_id': 7, 'delivery_id': 7, 'notification': 'Your package is out for delivery.'},
        {'user_id': 8, 'delivery_id': 8, 'notification': 'Your delivery is scheduled for tomorrow.'},
        {'user_id': 9, 'delivery_id': 9, 'notification': 'Your package has been dispatched from the sorting facility.'},
        {'user_id': 10, 'delivery_id': 10, 'notification': 'Your delivery has arrived at the final destination.'}
    ]

    for data in notifications_data:
        notification = UserNotification(user_id=data['user_id'], delivery_id=data['delivery_id'], notification=data['notification'])
        db.session.add(notification)

    db.session.commit()









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