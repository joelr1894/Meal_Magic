
import csv
from datetime import date, datetime, timedelta
import mysql.connector


def readCSVFile(filename):
	with open(filename, 'rb') as csv_file:
		reader = csv.reader(csv_file)
		return list(reader)

def load_data(cxn, cursor):
	UserData = readCSVFile("MealMagic_Data.csv")
	restaurants = UserData[0][1:]
	users = [u[0] for u in UserData[1:]]
	ratings = [u[1:] for u in UserData[1:]]
	
	for x in range(len(users)):
		cursor.execute(insert_users(), userDict(x, users[x]))
		cxn.commit()

	for rx in range(len(restaurants)):
		cursor.execute(insert_restaurants(), restDict(rx, restaurants[rx]))
		cxn.commit()

	for y in range(len(ratings)):
		for ry in range(len(restaurants)):
			cursor.execute(insert_ratings(), ratingDict(y, ry, int(ratings[y][ry])))
			cxn.commit()

	print "Finished ratings"


def userDict(user_id, user_name):
	userData = {
        'u_id': user_id,
        'Name' : user_name
    }
	return userData 

def insert_users():
# user ID and name
	value = ("INSERT INTO Users "
		"VALUES (%(u_id)s, %(Name)s)")
	return value


def restDict(rest_id, rest_name):
	restData = {
        'rest_id': rest_id,
        'rest_name' : rest_name
    }
	return restData

def insert_restaurants():
# rest ID and name
	value = ("INSERT INTO Restaurants "
		"VALUES (%(rest_id)s, %(rest_name)s)")
	return value


def ratingDict(user_id, rest_id, rating):
	ratingData = {
		'u_id': user_id,
		'rest_id': rest_id,
		'rating': rating
	}
	return ratingData

def insert_ratings():
# rating for each user ID/rest ID combo
	value = ("INSERT INTO ratings "
		"VALUES (%(u_id)s, %(rest_id)s), %(rating)s)")
	return value



def main():
	
	print "Starting connection"
	
	cnx = mysql.connector.connect(user='joelr', password='seniordesign', host='ec2-54-201-28-29.us-west-2.compute.amazonaws.com', database='Meal_Magic')
	cursor = cnx.cursor()
	
	print "Connected"
	
	load_data(cnx, cursor)


if __name__ == '__main__':
	main()
