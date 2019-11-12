#Library Imports

from flask import Flask, request, session, Response
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from flask_session import Session
import re
import base64
import json
import pickle
import csv

# Initial Setup

#Flask Setup
app = Flask(__name__)
api = Api(app)

#Session Setup
sess = Session()

#Mongo Setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/WTUsers_db"
mongo = PyMongo(app)

def convertCursor(info):
    data = []
    for x in info:
        data.append(x)
    return data	

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
		user_info = mongo.db.Users.find({}, {"_id": 0, "update_time": 0})
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
			uname = data.get("username")
			password = data.get("password")
			if(uname and password):
				x = mongo.db.Users.find({'username': uname})
				if(convertCursor(x)!=[]):
					return "Username Already Exists", 405
				else:
					mongo.db.Users.insert_one(data)
					return "Inserted", 201
			else:
				return "Invalid Credentials", 400
		
                        
	def delete(self, uname=None):
		data = []
		if(uname):
			user_info = mongo.db.Users.find({"username": uname})
			data = convertCursor(user_info)
			if(data==[]):
			    return 'user not found', 405
			else:
			    data = strip(data)
			    r = mongo.db.Users.remove({"username": uname})
			    return {}, 200
		else:
			return "Invalid Username", 400


class studentData(Resource):
    def get(self):
        Field = request.args.get('Field')
        pValue = request.args.get('pValue')
        allLines = []
        headers = []
        with open("../StudentData.csv", "r") as csvFile:
            reader = csv.reader(csvFile)
            headers = next(reader)
            for row in reader:
                allLines.append(row)

        if(int(Field)==1):
            retData = []
            for line in allLines:
                if(line[1].startswith(pValue)):
                    retData.append(line[1])
            return str(retData), 200

        if(int(Field)==2):
            retData = []
            for line in allLines:
                if(line[2].startswith(pValue)):
                    retData.append(line[2])
            return str(retData), 200

        if(int(Field)==3):
           for line in allLines:
                if((line[1].upper()==pValue.upper().strip("#")[0]) and (line[2].upper()==pValue.upper().strip("#")[1])):
                    return str(line), 200
           return "Student Not Found", 404
			
       
       
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

# Search Resource
api.add_resource(studentData, "/api/v1/search", endpoint="search");

#Predict Resource
api.add_resource(predictData, "/api/v1/predict", endpoint="predict")

# Run the App
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'mongodb'

    sess.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=70)
