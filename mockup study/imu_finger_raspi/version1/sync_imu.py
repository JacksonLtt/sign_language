import os, sys
import numpy as np
from scipy import signal

def convert(lines):

	lines = [line.replace('\n', '') for line in lines]
	lines = [line.split(',') for line in lines]
	# lines = [l.replace(' ', '') for line in lines for l in line]

	data = []
	for line in lines[1:]:
		temp = []
		for l in line:
			temp.append(float(l.replace(' ', '')))
		data.append(temp)

	# from accel_x1,accel_y1,accel_z1,mag_x1,mag_y1,mag_z1,gyro_x1,gyro_y1,gyro_z1
	# to accel_x1,accel_y1,accel_z1,gyro_x1,gyro_y1,gyro_z1, mag_x1,mag_y1,mag_z1
	data = np.array(data)
	# mag = data[:, [3,4,5]]
	# gyro = data[:, [6,7,8]]
    #
	# data[:, [3,4,5]] = gyro
	# data[:, [6,7,8]] = mag

	return data

def cut(data, s, tail=False):
	# print(data.shape)
	if tail == False and s != 0:
		data = data[:-s]
	elif tail == True and s != 0:
		data = data[s:]

	return data

# def sync(data,imu_data_dict):
# 	stimes = [v['stime'] for k, v in imu_data_dict.items()]
# 	etimes = [v['etime'] for k, v in imu_data_dict.items()]
# 	fss = [v['fs'] for k, v in imu_data_dict.items()]
#
#
# 	(left, right) = data
# 	print('Before: ', left.shape, right.shape)
#
# 	# lengths = [wrist.shape[0], thumb.shape[0], index.shape[0], ring.shape[0]]
#
# 	# print(stimes)
# 	max_idx, max_stime = np.argmax(stimes), stimes[np.argmax(stimes)]
# 	diff_stime = [int(abs(t - max_stime)* fss[idx]) for idx, t in enumerate(stimes)]
# 	print(diff_stime)
# 	#
# 	# print(diff_stime, " ", max_stime)
# 	#
# 	# print(etimes)
# 	min_idx, min_etime = np.argmin(etimes), etimes[np.argmin(etimes)]
# 	diff_etime = [int(abs(t - min_etime)* fss[idx]) for idx, t in enumerate(etimes)]
# 	print(diff_etime)
# 	# print(diff_etime, " ",min_etime)
#
# 	left = cut(left, diff_stime[0], tail=False)
# 	left = cut(left, diff_etime[0], tail=True)
#
# 	right = cut(right, diff_stime[1], tail=False)
# 	right = cut(right, diff_etime[1], tail=True)
#
#
# 	# print('After: ', left.shape, right.shape)
# 	print('After: ', left.shape, right.shape)
#
# 	min_len = min([left.shape[0], right.shape[0]])
#
# 	from scipy import signal
#
# 	left = signal.resample(left, min_len)
# 	right = signal.resample(right, min_len)
#
#
# 	print('Resample: ', left.shape, right.shape)
# 	return (left, right)

def sync_desample_cut(data,imu_data_dict):
	stimes = [v['stime'] for k, v in imu_data_dict.items()]
	etimes = [v['etime'] for k, v in imu_data_dict.items()]
	fss = [v['fs'] for k, v in imu_data_dict.items()]

	duration = [v['duration'] for k, v in imu_data_dict.items()]
	# print("stimes:",stimes)
	# print("etimes:",etimes)
	# print("fs:", fss)
	# print("duration:",duration)

	(left, right) = data

	print('Before: ', left.shape, right.shape)

	min_fs_dix, min_fs = np.argmin(fss), fss[np.argmin(fss)]


	left = signal.resample(left, int(min_fs*imu_data_dict['left']["duration"]))
	right = signal.resample(right, int(min_fs*imu_data_dict['right']["duration"]))

	print('After resample_fs: ', left.shape, right.shape)

	max_idx, max_stime = np.argmax(stimes), stimes[np.argmax(stimes)]
	min_idx, min_etime = np.argmin(etimes), etimes[np.argmin(etimes)]

	diff_stime = [int(abs(imu_data_dict['left']['stime']-max_stime)*min_fs),int(abs(imu_data_dict['right']['stime']-max_stime)*min_fs)]
	diff_etime = [int(abs(min_etime-imu_data_dict['left']['etime'])*min_fs),int(abs(min_etime-imu_data_dict['right']['etime'])*min_fs)]

	print(diff_stime)
	print(diff_etime)


	left = cut(left, diff_stime[0], tail=False)
	left = cut(left, diff_etime[0], tail=True)

	right = cut(right, diff_stime[1], tail=False)
	right = cut(right, diff_etime[1], tail=True)


	# print('After: ', left.shape, right.shape)
	print('After cut: ', left.shape, right.shape)

	min_len = min([left.shape[0], right.shape[0]])



	left = signal.resample(left, min_len)
	right = signal.resample(right, min_len)


	print('Resample: ', left.shape, right.shape)
	return (left, right)





def load_files(imu_data_dict):
	if "video" in imu_data_dict.keys():
		del imu_data_dict['video']
	if "ear" in imu_data_dict.keys():
		del imu_data_dict['ear']

	with open(imu_data_dict["left"]["path"], 'r') as f:
		lines = f.readlines()
	left = convert(lines)
	# print(left.shape)

	with open(imu_data_dict["right"]["path"], 'r') as f:
		lines = f.readlines()
	right = convert(lines)

	return sync_desample_cut((left,right),imu_data_dict)


def save_data(name, data):

	# np.savetxt(name, data, delimiter=',')

	final = []

	for line in data:
		temp = []
		for d in line:
			temp.append(str(d))

		final.append(','.join(temp))


	with open(name, 'w') as f:
		for line in final:
			f.write(line +'\n')





	print(name, " is saved!")
	# print(len(lines))




if __name__ == '__main__':
	## for hand imu
	imu_data = {"right": {"name": "right", "address": "F45E7C56-20A1-487C-AA49-9137616CFF97", "path": "/Users/taitinglu/Documents/GitHub/Ring/mockup study/experiment result/bob/right_unsync/bob_292_section1_right_unsync.txt",
						  "duration": 6.585643723999965,
						  "total": 544, "fs": 82.75576736923446, "stime": 69069.529011371, "etime": 69076.114655095}, "ear": {"name": "ear", "address": "24030208-6F3F-4F9A-BCB9-BC7C39F05388", "path": "/Users/taitinglu/Documents/GitHub/Ring/mockup study/experiment result/bob/ear/bob_292_section1_ear.txt", "duration": 6.859762868989492, "total": 572, "fs": 83.53058421163884, "stime": 69069.358752828, "etime": 69076.218515697},
				"left": {"name": "left", "address": "2A9F4C95-0B8A-4389-B697-834378A0A51B", "path": "/Users/taitinglu/Documents/GitHub/Ring/mockup study/experiment result/bob/left_unsync/bob_292_section1_left_unsync.txt",
						 "duration": 7.913877400002093,
						 "total": 656, "fs": 83.01872353997122, "stime": 69069.077347628, "etime": 69076.991225028}, "video": {"name": "video", "path": "/Users/taitinglu/Documents/GitHub/Ring/mockup study/experiment result/bob/videos/bob_292_section1.mp4", "duration": 6.23186646400427, "stime": 69069.846439387, "etime": 69076.078305851}}

	data = load_files(imu_data)
	save_data(imu_data["left"]["path"][:-11]+".txt", data[0])
	save_data(imu_data["right"]["path"][:-11]+".txt", data[1])






