import os, sys
import numpy as np
from scipy import signal



class SYNCIMU():
	def __init__(self,IMU_data):
		self.imu_data = IMU_data
		self.imu_keys = list(self.imu_data.keys())
		# print(self.imu_keys)
		self.left_name = self.imu_keys[0]
		self.right_name = self.imu_keys[1]


	def convert(self,lines):

		lines = [line.replace('\n', '') for line in lines]
		lines = [line.split(',') for line in lines]
		# lines = [l.replace(' ', '') for line in lines for l in line]

		data = []
		for line in lines[1:]:
			temp = []
			for l in line:
				temp.append(float(l.replace(' ', '')))
			data.append(temp)

		data = np.array(data)

		return data

	def cut(self,data, s, tail=False):
		# print(data.shape)
		if tail == False and s != 0:
			data = data[:-s]
		elif tail == True and s != 0:
			data = data[s:]

		return data

	def sync_desample_cut(self,data):
		stimes = [v['stime'] for k, v in self.imu_data.items()]
		etimes = [v['etime'] for k, v in self.imu_data.items()]
		fss = [v['fs'] for k, v in self.imu_data.items()]

		# print("stimes:",stimes)
		# print("etimes:",etimes)
		# print("fs:", fss)
		# print("duration:",duration)

		(left, right) = data

		print('Before: ', left.shape, right.shape)

		min_fs_dix, min_fs = np.argmin(fss), fss[np.argmin(fss)]

		left = signal.resample(left, int(min_fs * self.imu_data[self.left_name]["duration"]))
		right = signal.resample(right, int(min_fs * self.imu_data[self.right_name]["duration"]))

		print('After resample_fs: ', left.shape, right.shape)

		max_idx, max_stime = np.argmax(stimes), stimes[np.argmax(stimes)]
		min_idx, min_etime = np.argmin(etimes), etimes[np.argmin(etimes)]

		diff_stime = [int(abs(self.imu_data[self.left_name]['stime'] - max_stime) * min_fs),
					  int(abs(self.imu_data[self.right_name]['stime'] - max_stime) * min_fs)]
		diff_etime = [int(abs(min_etime - self.imu_data[self.left_name]['etime']) * min_fs),
					  int(abs(min_etime - self.imu_data[self.right_name]['etime']) * min_fs)]

		# print(diff_stime)
		# print(diff_etime)

		left = self.cut(left, diff_stime[0], tail=False)
		left = self.cut(left, diff_etime[0], tail=True)

		right = self.cut(right, diff_stime[1], tail=False)
		right = self.cut(right, diff_etime[1], tail=True)

		# print('After: ', left.shape, right.shape)
		print('After cut: ', left.shape, right.shape)

		min_len = min([left.shape[0], right.shape[0]])

		left = signal.resample(left, min_len)
		right = signal.resample(right, min_len)

		print('Resample: ', left.shape, right.shape)
		return (left, right)

	def load_files(self):

		with open(self.imu_data[self.left_name]["path"], 'r') as f:
			lines = f.readlines()
		left = self.convert(lines)

		with open(self.imu_data[self.right_name]["path"], 'r') as f:
			lines = f.readlines()
		right = self.convert(lines)

		return self.sync_desample_cut((left, right))

	def save_data(self,name, data):
		final = []

		for line in data:
			temp = []
			for d in line:
				temp.append(str(d))

			final.append(','.join(temp))

		with open(name, 'w') as f:
			for line in final:
				f.write(line + '\n')

		print(name, " is saved!")

# print(len(lines))
if __name__ == '__main__':
	## for hand imu
	imu_data = {"left#1": {"duration": 9.975306034088135,
						   "total": 828,
						   "fs": 83.10521974635145,
						   "stime": 1669865288.105068,
						   "etime": 1669865298.080374,
						   "name": "left#1",
						   "address": "2A9F4C95-0B8A-4389-B697-834378A0A51B",
						   "path": "/Users/taitinglu/Documents/GitHub/Ring/mockup study/experiment result/jack/left#1/jack_77_section2_left#1.txt"},
				"right#1": {"duration": 9.719534873962402,
							"total": 822,
							"fs": 84.67483379320231,
							"stime": 1669865288.098936,
							"etime": 1669865297.818471,
							"name": "right#1",
							"address": "F45E7C56-20A1-487C-AA49-9137616CFF97",
							"path": "/Users/taitinglu/Documents/GitHub/Ring/mockup study/experiment result/jack/right#1/jack_77_section2_right#1.txt"}}

	syncimu = SYNCIMU(imu_data)
	data = syncimu.load_files()
	syncimu.save_data("left#1.txt",data[0])
	syncimu.save_data("right#1.txt",data[0])








