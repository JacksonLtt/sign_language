# import numpy as np
import os, sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def visualize1D():
	fig, axs = plt.subplots(6, 9)
	fig.suptitle("1d projection")

	title = ["_".join(x.split("_")[:-1]) for x in header[1:10]]
	ylabels = ["wrist", "thumb", "index", "middle", "ring", "pinky"]
	
	# print(type(_finger))
	# print(_finger[1]['accl'])
	for kf, vf in _finger.items():
		axs[kf, 0].set_ylabel(ylabels[kf])
		for ks, vs in _sensor.items():
			for ka, va in _axis.items():
				axs[kf, ks*3+ka].plot(vf[vs][va])
				if kf == 0:
					axs[kf, ks*3+ka].set_title(title[ks*3+ka])

	plt.show()



def visualize_mag():
	print(_finger)
	# fig, axs = plt.subplots(1, 3)
	# fig.suptitle("1d projection")
	#
	# title = ["_".join(x.split("_")[:-1]) for x in header2[1:10]]
	# ylabels = ["wrist", "thumb", "index", "middle", "ring", "pinky"]
	#
	# for kf, vf in _finger.items():
	# 	axs[kf, 0].set_ylabel(ylabels[kf])
	# 	for ks, vs in _sensor.items():
	# 		for ka, va in _axis.items():
	# 			axs[kf, ks * 3 + ka].plot(vf[vs][va])
	# 			if kf == 0:
	# 				axs[kf, ks * 3 + ka].set_title(title[ks * 3 + ka])
	#
	# plt.show()

# header2 = ["time_stamp",\
#
# 	"accel_x_0", "accel_y_0", "accel_z_0",\
# 	"mag_x_0"  , "mag_y_0"  , "mag_z_0"  ,\
# 	"gyro_x_0" , "gyro_y_0" , "gyro_z_0" ]

header = ["time_stamp",\

	"accel_x_0", "accel_y_0", "accel_z_0",\
	"mag_x_0"  , "mag_y_0"  , "mag_z_0"  ,\
	"gyro_x_0" , "gyro_y_0" , "gyro_z_0" ,\

	"accel_x_1", "accel_y_1", "accel_z_1",\
	"mag_x_1"  , "mag_y_1"  , "mag_z_1"  ,\
	"gyro_x_1" , "gyro_y_1" , "gyro_z_1" ,\

	"accel_x_2", "accel_y_2", "accel_z_2",\
	"mag_x_2"  , "mag_y_2"  , "mag_z_2"  ,\
	"gyro_x_2" , "gyro_y_2" , "gyro_z_2" ,\

	"accel_x_3", "accel_y_3", "accel_z_3",\
	"mag_x_3"  , "mag_y_3"  , "mag_z_3"  ,\
	"gyro_x_3" , "gyro_y_3" , "gyro_z_3" ,\

	"accel_x_4", "accel_y_4", "accel_z_4",\
	"mag_x_4"  , "mag_y_4"  , "mag_z_4"  ,\
	"gyro_x_4" , "gyro_y_4" , "gyro_z_4" ,\

	"accel_x_5", "accel_y_5", "accel_z_5",\
	"mag_x_5"  , "mag_y_5"  , "mag_z_5"  ,\
	"gyro_x_5" ,"gyro_y_5"  , "gyro_z_5" ]



# def readcsv(file):
# 	root = os.path.dirname(os.path.abspath(__file__)) + "/"
# 	file = root + file
# 	print(file)

# 	df = pd.read_csv(file)
# 	# print(df.columns)

# 	# print(df["time_stamp"].values)

# 	global ts, thumb, index, middle, ring, pinky
	
# 	ts = df["time_stamp"].values

# 	thumb = {
# 		"accl": dict(),
# 		"mag" : dict(),
# 		"gyro": dict(),
# 	}

# 	index = {
# 		"accl": dict(),
# 		"mag" : dict(),
# 		"gyro": dict(),
# 	}

# 	middle = {
# 		"accl": dict(),
# 		"mag" : dict(),
# 		"gyro": dict(),
# 	}
# 	ring = {
# 		"accl": dict(),
# 		"mag" : dict(),
# 		"gyro": dict(),
# 	}

# 	pinky = {
# 		"accl": dict(),
# 		"mag" : dict(),
# 		"gyro": dict(),
# 	}

# 	global _finger, _sensor, _axis

# 	_finger = {
# 		0: thumb,
# 		1: index,
# 		2: middle,
# 		3: ring,
# 		4: pinky,
# 	}

# 	_sensor = {
# 		0: "accl",
# 		1: "mag",
# 		2: "gyro",
# 	}

# 	_axis = {
# 		0: "x",
# 		1: "y",
# 		2: "z",
# 	}

# 	for i, name in enumerate(header[1:]):
# 		_finger[i//9][_sensor[(i%9)//3]][_axis[i%3]] = df[name].values



def checkSampling(ts):
	diff = []

	x = np.linspace(0, 1, ts.shape[0]-1)

	for i in range(ts.shape[0]-1):
		diff.append((ts[i+1] - ts[i])/1000)
		# print((ts[i+1] - ts[i]))

	# plt.plot(x, diff, 'o', color='black')
	# print(min(diff))
	# print(sorted(diff))
	# sorted_diff = sorted(diff)
	# print(sorted_diff)
	# print(sum(sorted_diff)/len(sorted_diff))
	# plt.ylim([0,20])
	# plt.show()


def readtxt(file):
	root = os.path.dirname(os.path.abspath(__file__)) + "/"
	file = root + file

	with open(file, "r") as f:
		lines = f.readlines()
	f.close()

	samples = []

	for line in lines:
		line = line.rstrip()[1:-1] # get rid of [ ]
		if len(line) == 0:
			continue
		else:
			line = line.split(",")
			# print(line)
			samples.append([float(i) for i in line])

	# print(samples)

	samples = np.array(samples)

	print(samples.shape)

	global ts, wrist, thumb, index, middle, ring, pinky
	
	ts = samples[:, 54]

	checkSampling(ts)

	wrist = {
		"accl": dict(),
		"mag" : dict(),
		"gyro": dict(),
	}

	thumb = {
		"accl": dict(),
		"mag" : dict(),
		"gyro": dict(),
	}

	index = {
		"accl": dict(),
		"mag" : dict(),
		"gyro": dict(),
	}

	middle = {
		"accl": dict(),
		"mag" : dict(),
		"gyro": dict(),
	}
	ring = {
		"accl": dict(),
		"mag" : dict(),
		"gyro": dict(),
	}

	pinky = {
		"accl": dict(),
		"mag" : dict(),
		"gyro": dict(),
	}

	global _finger, _sensor, _axis

	_finger = {
		0: wrist,
		1: thumb,
		2: index,
		3: middle,
		4: ring,
		5: pinky,
	}

	_sensor = {
		0: "accl",
		1: "mag",
		2: "gyro",
	}

	_axis = {
		0: "x",
		1: "y",
		2: "z",
	}

	for i, _ in enumerate(range(samples.shape[1]-1)):
		_finger[i//9][_sensor[(i%9)//3]][_axis[i%3]] = samples[:, i+1]


if __name__ == "__main__":

	file = None
	if len(sys.argv) == 1:
		file = "7.txt"
	else:
		file = sys.argv[1]
	# readcsv(file)
	readtxt(file)
	visualize1D()


