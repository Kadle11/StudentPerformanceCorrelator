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
from matplotlib import pyplot as plt
import pandas as pd

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

				x = mongo.db.Users.find({'username': uname, 'password': password})

				if(x.count()==0):
					return "Enter Valid Credentials", 405

				else:
					return "Authorization Successful", 200


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
				if(x.count()!=0):
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

    def post(self):
        data = request.get_json()
        row = []
        with open("../StudentData.csv", "r") as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            allLines = []
            for rowX in reader:
                allLines.append(rowX[0])
            row.append(int(allLines[-1])+1)
        row.append(data.get("FName"));
        row.append(data.get("LName"));
        row.append(data.get("Math"));
        row.append(data.get("Chem"));
        row.append(data.get("Bio"));
        row.append(data.get("CS"));
        row.append(data.get("Sports"));
        with open("../StudentData.csv", "a") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
        return "Inserted", 200

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



class correlateData(Resource):
	def get(self):
		S1 = request.args.get('S1')
		S2 = request.args.get('S2')
		df = pd.read_csv('../StudentData.csv')
		fig, ax = plt.subplots()
		ax.grid(True)
		plt.xlabel(S1)
		plt.ylabel(S2)
		plt.xlim(0, 100)
		plt.ylim(0, 100)
		plt.scatter(df[S1], df[S2])
		fig.savefig("/var/www/html/Plots/"+S1+"_vs_"+S2+".png")
		#To access the Image go to http://localhost/<The URL in the Respose>	
		return str(df.corr(method='pearson')[S1][S2])+", Plots/"+S1+"_vs_"+S2+".png", 200

		

		

# Resources for User
api.add_resource(Login, "/api/v1/login", endpoint="Login")
api.add_resource(User, "/api/v1/users", endpoint="Add User")
api.add_resource(User, "/api/v1/users/<string:uname>", endpoint="Delete User")

# Search Resource
api.add_resource(studentData, "/api/v1/search", endpoint="Search");

#Add Student Resource
api.add_resource(studentData, "/api/v1/student", endpoint="Add Student");

#Predict Resource
api.add_resource(predictData, "/api/v1/predict", endpoint="Predict")

#Correlate Resource
api.add_resource(correlateData, "/api/v1/correlate", endpoint="Correlate")

# Run the App
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'mongodb'

    sess.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=70)
