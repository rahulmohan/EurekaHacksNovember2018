import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
from collections import Counter
from math import sin, cos, sqrt, atan2, radians

bike_may = pd.read_csv("201805-fordgobike-tripdata.csv.zip")
bike_jun = pd.read_csv("201806-fordgobike-tripdata.csv.zip")
bike_jul = pd.read_csv("201807-fordgobike-tripdata.csv.zip")
bike_aug = pd.read_csv("201808-fordgobike-tripdata.csv.zip")
bike_sep = pd.read_csv("201809-fordgobike-tripdata.csv.zip")
all_months = pd.concat([bike_may, bike_jun, bike_jul, bike_aug, bike_sep])

def get_station_names_from_id(all_data, ids):
	station_ids = all_data.start_station_id.values
	station_names = all_data.start_station_name.values
	for id in ids:
		id_idx = np.where(station_ids == id)[0][0]
		print("ID: " + str(id) + ", Station Name: " + station_names[id_idx])

def most_popular_stations(bike_data):
	most_common_start = bike_data.start_station_id.value_counts()
	most_common_end = bike_data.end_station_id.value_counts()
	most_common_start = most_common_start.iloc[0:10]
	most_common_end = most_common_end.iloc[0:10]
	
	index = np.arange(len(most_common_start))
	ticks = most_common_start.index.tolist()
	heights = most_common_start.values

	fig, ax = plt.subplots()
	rects1 = ax.bar(index, heights, color='b', label='Frequency', align='edge', width=0.5)
	ax.set_xlabel('Starting stations')
	ax.set_ylabel('Frequency')
	ax.set_title('Most popular starting destinations')
	ax.set_xticks(index + 0.6 / 2)
	ax.set_xticklabels(ticks)
	ax.legend()
	fig.tight_layout()
	plt.savefig("most_popular_start_stations.png")

	index = np.arange(len(most_common_end))
	ticks = most_common_end.index.tolist()
	heights = most_common_end.values

	fig, ax = plt.subplots()
	rects1 = ax.bar(index, heights, color='b', label='Frequency', align='edge', width=0.5)
	ax.set_xlabel('Ending stations')
	ax.set_ylabel('Frequency')
	ax.set_title('Most popular ending destinations')
	ax.set_xticks(index + 0.6 / 2)
	ax.set_xticklabels(ticks)
	ax.legend()
	fig.tight_layout()
	plt.savefig("most_popular_end_stations.png")

	print("Success!")

def most_popular_route(all_data):
	route_tuples = []
	starting_dest = all_data["start_station_name"].values
	ending_dest = all_data["end_station_name"].values
	for i in range(len(starting_dest)):
		route_tuples.append([starting_dest[i], ending_dest[i]])
	route_tuples = map(tuple, route_tuples)
	final_count = Counter(route_tuples).most_common(10)
	
	for route in final_count:
		dest = route[0]
		if type(dest[0]) == float:
			continue
		else:
			print "Starting dest: " + str(dest[0]) + ", Ending dest: " + str(dest[1]) + ", Frequency: " + str(route[1])

def long_lat_to_dist(start_lon, start_lat, end_lon, end_lat):
	# approximate radius of earth in km
	R = 6373.0
	lat1 = radians(start_lon)
	lon1 = radians(start_lat)
	lat2 = radians(end_lon)
	lon2 = radians(end_lat)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	return distance

def avg_distance(all_data):
	starting_lon = all_data["start_station_longitude"].values
	starting_lat = all_data["start_station_latitude"].values
	ending_lon = all_data["end_station_longitude"].values
	ending_lat = all_data["end_station_latitude"].values
	dist = []
	for i in range(len(starting_lon)):
		if (starting_lon[i] == np.nan) or (starting_lat[i] == np.nan) or (ending_lon[i] == np.nan) or (ending_lat[i] == np.nan):
			continue
		else:
			dist.append(long_lat_to_dist(starting_lon[i], starting_lat[i], ending_lon[i], ending_lat[i]))
	print("Average distance travelled: " + str(np.mean(dist)) + " km")

def avg_duration(all_data):
	duration = all_data["duration_sec"].values
	print ("Average duration (seconds): " + str(np.mean(duration)))

def calc_peak_hours(all_data):
	hours = []
	starting_times = all_data["start_time"].values
	for i in range(len(starting_times)):
		hours.append(pd.to_datetime(starting_times[i]).hour)
	counter = dict(Counter(hours))	
	labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
	bins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	fig, ax = plt.subplots()
	ax.hist(hours, bins=bins)
	ax.set_xlabel('Hour')
	ax.set_ylabel('Frequency')
	ax.set_title('Peak Hours of Bike Sharing Demand')
	ax.set_xticks(np.array(bins))
	ax.set_xticklabels(labels)
	plt.savefig("peak_demand_hist.png")
	print("Success!")

def compare_groups(all_data):
	user_types = all_data['user_type'].values
	gender = all_data['member_gender'].values
	# user type pie chart
	type_counts = [len(np.where(user_types == "Customer")[0]), len(np.where(user_types == "Subscriber")[0])]
	type_labels = ["Customer", "Subscriber"]
	plt.pie(type_counts, labels=type_labels, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.savefig("user_type_piechart.png")
	plt.close()
	# gender pie chart
	type_counts = [len(np.where(gender == "Male")[0]), len(np.where(gender == "Female")[0])]
	type_labels = ["Male", "Female"]
	plt.pie(type_counts, labels=type_labels, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.savefig("user_gender_piechart.png")

def get_age_dist(all_data):
	ages = []
	birth_years = all_data['member_birth_year'].dropna().values
	for birth_year in birth_years:
		if (birth_year == np.nan):
			continue
		else:
			ages.append(2018 - birth_year)
	fig, ax = plt.subplots()
	ax.hist(ages)
	ax.set_xlabel('Age')
	ax.set_ylabel('Frequency')
	ax.set_title('Age Distribution of Bike Share Users')
	plt.savefig("age_distribution_hist.png")

most_popular_stations(all_months)
most_popular_route(all_months)
avg_distance(all_months)
avg_duration(all_months)
calc_peak_hours(all_months)
compare_groups(all_months)
get_age_dist(all_months)
#get_station_names_from_id(all_months, [15.0, 67.0, 6.0, 30.0, 21.0, 81.0, 58.0, 3.0, 16.0, 22.0])

