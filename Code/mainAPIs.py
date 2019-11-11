#Library Imports

from flask import Flask, request, session, Response
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from flask_session import Session
import re
import base64
import json
import pickle

# Initial Setup


#Flask Setup
app = Flask(__name__)
api = Api(app)

#Session Setup
sess = Session()

#Login Class
class Login(Resource):

	def post(self):
		data = request.get_json()

		if(not(data)):
			return "ERROR", 400

		else:

			uname = data.get('username')
			password = data.get('password')

			if(not(uname and password)):
				return "Enter Valid Credentials", 400

			else:

				x = mongo.db.user.find({'username': uname, 'password': password})
				y = convertCursor(x)

				if(y==[]):
					return "Enter Valid Credential", 405

				else:
					return {}, 200


# User Class
class User(Resource):

	def get(self, uname=None):
		if(uname):
			return "", 405
		user_info = mongo.db.user.find({}, {"_id": 0, "update_time": 0})
		user_list = []
		for user in user_info:
			user_list.append(user["username"])
		if(user_list == []):
			return "No Users", 204
		return user_list, 200


	
	def post(self, uname=None):
		if(uname):
			return "", 405
		data = request.get_json()
		if(not(data)):
			return "ERROR", 400
		else:
		    uname = data.get('username')
		    password = data.get('password')
		    if(uname and password):
		        if(checkSHA1(password)):
		            x = mongo.db.user.find({'username': uname})
		            y = convertCursor(x)
		            if(y!=[]):
		                return "username already exists.", 405
		            else:
		                mongo.db.user.insert_one(data)
		                return {}, 201
		        else:
		        	return "password is not SHA", 400
		    else:
		    	return "username or password missing", 400
		        

	def delete(self, uname=None):
		data = []
		if(uname):
			user_info = mongo.db.user.find({"username": uname})
			data = convertCursor(user_info)
			if(data==[]):
			    return 'user not found', 405
			else:
			    data = strip(data)
			    r = mongo.db.user.remove({"username": uname})
			    return {}, 200
		else:
			return "Invalid Username", 400


#Predict Class
class predictData(Resource):

    def get(self):

        Subject = request.args.get('Subject')
        Value = float(request.args.get('Score'))
        if(Value < 0):
            return "Invalid Score", 400
        
        if(Subject.upper()==("MATH")):
            CM = pickle.load(open('../Models/CM.pkl', 'rb'));
            MS = pickle.load(open('../Models/MS.pkl', 'rb'));
            CompScore = CM.predict([[float(Value)]])[0][0];
            Sports = MS.predict([[float(Value)]])[0];
            return "CompScience: "+str(CompScore)+", Sports: "+str(Sports), 200
        
        if(Subject.upper()==("COMPUTER SCIENCE")):
            MC = pickle.load(open('../Models/MC.pkl', 'rb'));
            SC = pickle.load(open('../Models/SC.pkl', 'rb'));
            MathScore = MC.predict([[float(Value)]])[0][0];
            Sports = SC.predict([[float(Value)]])[0];
            return "Math: "+str(MathScore)+", Sports: "+str(Sports), 200
            
        if(Subject.upper()==("CHEMISTRY")):
            CB = pickle.load(open('../Models/CB.pkl', 'rb'));
            BioScore = CB.predict([[float(Value)]])[0][0];
            return "Bio: "+str(BioScore), 200

        if(Subject.upper()==("BIOLOGY")):
            BC = pickle.load(open('../Models/BC.pkl', 'rb'));
            ChemScore = BC.predict([[float(Value)]])[0][0];
            return "Chem: "+str(ChemScore), 200

        else:
            return "Invalid Subject", 405



# Resources for User
api.add_resource(Login, "/api/v1/login", endpoint="login")
api.add_resource(User, "/api/v1/users", endpoint="add user")
api.add_resource(User, "/api/v1/users/<string:uname>", endpoint="delete")


#Predict Resource
api.add_resource(predictData, "/api/v1/predict", endpoint="predict")

# Run the App
if __name__ == "__main__":
    app.secret_key = 'super secret key'

    sess.init_app(app)
    print("Point A")
    app.run(debug=False, host="0.0.0.0", port=1000)
