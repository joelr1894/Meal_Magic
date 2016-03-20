import csv
from datetime import date, datetime, timedelta
import mysql.connector

# Reads in the csv file and returns a list of lists of the data where the 
# inner list is the row

def import_function():
	print "Starting connection"
	cnx = mysql.connector.connect(user='joelr', password='seniordesign', host='ec2-54-201-28-29.us-west-2.compute.amazonaws.com', database='Meal_Magic')
	cursor = cnx.cursor()
	print "Connected"
	
	user_query = ("SELECT * from Users")
	cursor.execute(user_query)
	user_dict = dict()
	for (user_id, user_name) in cursor:
		user_dict[user_id] = user_name

	rest_query = ("SELECT * from Restaurants")
	cursor.execute(rest_query)
	rest_dict = dict()
	for (rest_id, rest_name) in cursor:
		rest_dict[rest_id] = rest_name

	rest_list = [0]*(len(rest_dict.keys())+1)
	rest_list[0] = ""
	for i in rest_dict.keys():
		rest_list[i+1] = str(rest_dict[i])

	print rest_list
	rating_csv = [rest_list]

	rate_query = ("SELECT * from ratings")
	cursor.execute(rate_query)
	rate_dict = dict()
	for i in range(len(user_dict)):
		rate_dict[i] = []
	for (rate_u_id, rate_rest_id, rating) in cursor:
		rate_dict[rate_u_id].append((rate_rest_id, rating))

	for user in user_dict.keys():
		user_rating_list = [0]*(len(rest_dict.keys())+1)
		user_rating_list[0] = str(user_dict[user])
		for rating_pair in rate_dict[user]:
			user_rating_list[rating_pair[0]+1] = rating_pair[1]
		print user_rating_list
		rating_csv.append(user_rating_list)	
		
	print rating_csv
	return rating_csv

def readCSVFile(filename):
    # with open(filename, 'rb') as csv_file:
    #     reader = csv.reader(csv_file)
    #     return list(reader)
    return import_function()

def input_function():
	print ""
	user = raw_input("What is your name? ")
	recs = int(raw_input('How many recommendations do you want? '))
	inputs = [user, recs, 20, 4, 10]
	return inputs

# Counts the number and names of restaurants that the given user has not 
# visited (where a 0 in the rating siginifies not visiting)
def count_not_visited(l, restaurants):
	count = 0
	rest = []
	rest_num = []
	for i in range(len(l)):
		if int(l[i]) == 0:
			count = count + 1
			rest.append(restaurants[i])
			rest_num.append(i)
	return count, rest, rest_num

# Given the ratings of two users, distance finds the average distance in score
# between the two users based on the restaurants that they've both visited 
# and rated
def distance(user1, user2):
	counter = 0
	distance = 0
	for r in range(len(user1)):
		if user1[r] != 0 and user2[r] != 0:
			counter = counter + 1
			distance = distance + abs(user1[r] - user2[r])
	if counter == 0:
		return float(100)
	return float(distance)/counter

def nearest_neighbors(user1,critics,inputs):
	neighbors = []
	temp_avg_distance = dict(critics[user1][3])
	while len(neighbors) < inputs[2]:
		temp_min = min(temp_avg_distance, key=temp_avg_distance.get)
		if (len(critics[user1][0]) - critics[temp_min][1]) > inputs[4]:
			neighbors.append(temp_min)
		temp_avg_distance[temp_min] = float(100)
	return neighbors

def neighbor_array(critics,neighbors):
	nn_array = dict()
	for i in neighbors:
		nn_array[i] = critics[i][0]
	return nn_array

def nn_restaurant_ratings(nn_array):
	neighbor_ratings = []
	num_visited = []
	for n in nn_array:
		temp_key = n
	for r in range(len(nn_array[temp_key])):
		neighbor_ratings.append(0)
		num_visited.append(0)
		for i in nn_array:
			if nn_array[i][r] != 0:
				num_visited[r] = num_visited[r] + 1
			neighbor_ratings[r] = neighbor_ratings[r] + nn_array[i][r]
		if num_visited[r] != 0:
			neighbor_ratings[r] = float(neighbor_ratings[r]) / num_visited[r]
	return neighbor_ratings, num_visited

# Gives recommendation after removing restaurants with too few visits and
# restaurants the user has already visited
def recommend(neighbors,inputs,not_visited):
	temp_ratings = dict()
	# Populates temp_ratings with restaurants not visited by user
	for n in range(len(neighbors[2])):
		for i in not_visited:
			if n == i:
				temp_ratings[n] = neighbors[2][n]
	# Zeros out restaurants with too few visits
	for x in range(len(neighbors[2])):
		if neighbors[3][x] < inputs[3]:
			temp_ratings[x] = 0
	# Gets highest rated restaurants as recommendations
	recommendations = []
	for i in range(inputs[1]):
		recommendations.append(max(temp_ratings, key=temp_ratings.get))
		temp_ratings[recommendations[i]] = 0
		i = i + 1

	return recommendations, temp_ratings

def print_out(recommendation, neighbors, output, inputs):
	print ''
	print inputs[0] + ', your restaurant recommendations are:'
	for i in range(inputs[1]):
		print output[inputs[0]][i] + ' with a rating of ' + str(round(neighbors[inputs[0]][2][recommendation[inputs[0]][0][i]],1))
		i = i + 1
	print ''
	print inputs[0] + ', your nearest neighbors are:'
	print neighbors[inputs[0]][0]
	return

def main():
	# Gather inputs
	# (user name,
	#  num recommendations,
	#  num of nearest neighbors,
	#  min num of visits from neighbors
	#  min num of restaurants visited for nn calc)
	inputs = input_function()
	# Import the data
	meal_ratings = readCSVFile("MealMagic_data3.csv")
	# initialize the map of users to their information
	critics = dict()
	# initialize the map of users to the restaurant numbers not visited
	not_visited = dict()
	# initialize the maps of users to their neighbor information
	neighbors = dict()
	nn = dict()
	nn_array = dict()
	rr_temp = dict()
	# initialize the map of users to their recommendations
	recommendation = dict()
	# initialize the output of restaurant names
	output = dict()
	# All of the restaurant names
	restaurants = meal_ratings[0][1:]

	# for each user...
	for i in range(1, len(meal_ratings)):
		# Find the number of restaurants not visited and their names
		counts = count_not_visited(meal_ratings[i][1:], restaurants)

		# cast the strings parsed from the csv into meaningful integers
		cast_ints = []
		for j in range(1, len(meal_ratings[i])):
			cast_ints.append(int(meal_ratings[i][j]))

		# populate the initial critics dictionary 
		# (ratings, # rests not visits, names of restaurants not visited)
		critics[meal_ratings[i][0]] = (cast_ints, counts[0], counts[1])

		#populate the dictionary of restaurant numbers not visited
		not_visited[meal_ratings[i][0]] = (counts[2])


	# for each user, find their distance to all of the other users
	# k is the base user
	for k in critics.keys():
		distances = dict()
		counter = dict()
		# k2 iterates through the rest of the users
		for k2 in critics.keys():
			if k2 != k:
				# find the distances
				distances[k2] = distance(critics[k][0], critics[k2][0])
		# update the critics map
		# (ratings, 
		#  number of restaurants not visited, 
		#  names of restaurants not visited, 
		#  map of other users and this user's distance to them,
		#  map of other users and the number of restaurants both have rated)
		critics[k] = critics[k][0],critics[k][1],critics[k][2], distances, counter

	
		# find nearest neighbors for each user
		nn[k] = nearest_neighbors(k,critics,inputs)
		# create array of neighbor ratings
		nn_array[k] = neighbor_array(critics,nn[k])
		# calculate ratings and number of visits for each restaurant
		rr_temp[k] = nn_restaurant_ratings(nn_array[k])
		# update neighbors map
		# (nearest neighbor names,
		#  array of neighbor ratings,
		#  average restaurant ratings from neighbors,
		#  number of visits to each restaurant from neighbors)
		neighbors[k] = (nn[k], nn_array[k], rr_temp[k][0], rr_temp[k][1])

		# gives recommendation restaurant numbers
		recommendation[k] = recommend(neighbors[k],inputs,not_visited[k])
		output[k] = []
		for i in recommendation[k][0]:
			output[k].append(restaurants[i])
	print_out(recommendation, neighbors, output, inputs) 

	# Testing for inf bug
	# print critics['Dan Haroun'][3]['Matt Schulman']
	# print distance(critics['Dan Haroun'][0], critics['Matt Schulman'][0])
	# print distances['Matt Schulman']

if __name__ == '__main__':
    main()

