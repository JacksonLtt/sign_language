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

def visualize1D_2IMU():
	fig, axs = plt.subplots(2, 9)
	fig.suptitle("1d projection")

	title = ["_".join(x.split("_")[:-1]) for x in header[1:10]]
	ylabels = ["left", "right"]

	# print(type(_finger))
	# print(_finger[1]['accl'])
	for kf, vf in _finger.items():
		axs[kf, 0].set_ylabel(ylabels[kf])
		for ks, vs in _sensor.items():
			for ka, va in _axis.items():
				axs[kf, ks * 3 + ka].plot(vf[vs][va])
				if kf == 0:
					axs[kf, ks * 3 + ka].set_title(title[ks * 3 + ka])

	plt.show()

def visualize1D_1IMU():
	fig, axs = plt.subplots(1, 9)
	fig.suptitle("1d projection")

	title = ["_".join(x.split("_")[:-1]) for x in header[1:10]]
	ylabels = ["left"]

	for kf, vf in _finger.items():
		axs[kf].set_ylabel(ylabels[kf])
		for ks, vs in _sensor.items():
			for ka, va in _axis.items():
				axs[ks * 3 + ka].plot(vf[vs][va])
				if kf == 0:
					axs[ks * 3 + ka].set_title(title[ks * 3 + ka])

	plt.show()

header = ["time_stamp",\

	"accel_x_0", "accel_y_0", "accel_z_0",\
	"gyro_x_0" , "gyro_y_0" , "gyro_z_0" ,\
	"mag_x_0"  , "mag_y_0"  , "mag_z_0"  ,\
	]



def readtxt_2IMU(file):
	file = file

	with open(file, "r") as f:
		lines = f.readlines()
	f.close()

	samples = []

	for line in lines:
		line = line.rstrip()[1:-1]  # get rid of [ ]
		if len(line) == 0:
			continue
		else:
			line = line.split(",")
			# print(line)
			samples.append([float(i) for i in line])

	# print(samples)

	samples = np.array(samples)

	print(samples.shape)

	global ts, left, right

	ts = samples[:, 18]

	# checkSampling(ts)

	left = {
		"accl": dict(),
		"mag": dict(),
		"gyro": dict(),
	}

	right = {
		"accl": dict(),
		"mag": dict(),
		"gyro": dict(),
	}



	global _finger, _sensor, _axis

	_finger = {
		0: left,
		1: right,
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

	for i, _ in enumerate(range(samples.shape[1] - 1)):
		_finger[i // 9][_sensor[(i % 9) // 3]][_axis[i % 3]] = samples[:, i]

def readtxt_1IMU(file):
	file = file

	with open(file, "r") as f:
		lines = f.readlines()
	f.close()

	samples = []

	for line in lines:
		# line = line.rstrip()[1:-1]  # get rid of [ ]
		if len(line) == 0:
			continue
		else:
			line = line.split(",")
			# print(line)
			samples.append([float(i) for i in line])

	# print(samples)

	samples = np.array(samples)

	print(samples.shape)

	global ts, left

	ts = samples[:, 9]

	# checkSampling(ts)

	left = {
		"accl": dict(),
		"gyro": dict(),
		"mag": dict(),
	}



	global _finger, _sensor, _axis

	_finger = {
		0: left
	}

	_sensor = {
		0: "accl",
		1: "gyro",
		2: "mag",
	}

	_axis = {
		0: "x",
		1: "y",
		2: "z",
	}

	for i, _ in enumerate(range(samples.shape[1] - 1)):
		_finger[i // 9][_sensor[(i % 9) // 3]][_axis[i % 3]] = samples[:, i]


if __name__ == "__main__":

	if len(sys.argv) == 1:

		file = "tennis4.txt"

		readtxt_1IMU(file)
		visualize1D()





