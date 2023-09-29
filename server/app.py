#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api, bcrypt
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    def post(self):
        
        username = request.get_json()['username']
        password = request.get_json()['password']

        if username and password:

            new_user = User(username=username)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return new_user.to_dict(), 201
        return {'error': '422: Unprocessable Entity'}, 422

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user=User.query.filter(User.id == session['user_id']).first()

            return user.to_dict(), 200
        return {}, 204

class Login(Resource):
    def post(self):
        json_data = request.get_json()

        # Extract user data from JSON request
        username = json_data.get('username')
        password = json_data.get('password')

        # Find the user by username
        user = User.query.filter_by(username=username).first()

        if user:
            # Check if the provided password matches the stored hash
            if user.authenticate(password):
                # User is authenticated, store the user's ID in the session
                session['user_id'] = user.id
                return user.to_dict()

        # If the user is not found or the password is incorrect, return an error message
        return {"message": "Invalid credentials"}, 401



class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
