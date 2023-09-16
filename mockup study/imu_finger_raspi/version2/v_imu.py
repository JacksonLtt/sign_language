# import numpy as np
import os, sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def visualize_6IMU():
    fig, axs = plt.subplots(6, 9)
    fig.suptitle("1d projection")

    title = ["_".join(x.split("_")[:-1]) for x in zip_header[1:10]]
    ylabels = ["wrist", "thumb", "index", "middle", "ring", "pinky"]

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


zip_header = ["time_stamp",
          "accel_x_0", "accel_y_0", "accel_z_0", \
          "mag_x_0", "mag_y_0", "mag_z_0", \
          "gyro_x_0", "gyro_y_0", "gyro_z_0", \
 \
          "accel_x_1", "accel_y_1", "accel_z_1", \
          "mag_x_1", "mag_y_1", "mag_z_1", \
          "gyro_x_1", "gyro_y_1", "gyro_z_1", \
 \
          "accel_x_2", "accel_y_2", "accel_z_2", \
          "mag_x_2", "mag_y_2", "mag_z_2", \
          "gyro_x_2", "gyro_y_2", "gyro_z_2", \
 \
          "accel_x_3", "accel_y_3", "accel_z_3", \
          "mag_x_3", "mag_y_3", "mag_z_3", \
          "gyro_x_3", "gyro_y_3", "gyro_z_3", \
 \
          "accel_x_4", "accel_y_4", "accel_z_4", \
          "mag_x_4", "mag_y_4", "mag_z_4", \
          "gyro_x_4", "gyro_y_4", "gyro_z_4", \
 \
          "accel_x_5", "accel_y_5", "accel_z_5", \
          "mag_x_5", "mag_y_5", "mag_z_5", \
          "gyro_x_5", "gyro_y_5", "gyro_z_5",
    ]


def readtxt_6IMU(samples):
    global ts, wrist, thumb, index, middle, ring, pinky
    ts = samples[:, 54]

    # checkSampling(ts)

    wrist = {
        "accl": dict(),
        "mag": dict(),
        "gyro": dict(),
    }

    thumb = {
        "accl": dict(),
        "mag": dict(),
        "gyro": dict(),
    }

    index = {
        "accl": dict(),
        "mag": dict(),
        "gyro": dict(),
    }

    middle = {
        "accl": dict(),
        "mag": dict(),
        "gyro": dict(),
    }
    ring = {
        "accl": dict(),
        "mag": dict(),
        "gyro": dict(),
    }

    pinky = {
        "accl": dict(),
        "mag": dict(),
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
        # print(i,_)
        _finger[i // 9][_sensor[(i % 9) // 3]][_axis[i % 3]] = samples[:, i]


def visualize_2IMU():
    fig, axs = plt.subplots(2, 9)
    fig.suptitle("1d projection")

    title = ["_".join(x.split("_")[:-1]) for x in ear_header[1:10]]
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

ear_header = ["time_stamp",\
    "accel_x_0", "accel_y_0", "accel_z_0",\
    "gyro_x_0" , "gyro_y_0" , "gyro_z_0" ,\
    "mag_x_0"  , "mag_y_0"  , "mag_z_0"  ,\
    ]

def readTXT(file):
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

    samples = np.array(samples)

    print(samples.shape)
    if samples.shape[1] == 55:
        readtxt_6IMU(samples)
        visualize_6IMU()
    elif samples.shape[1] == 19:
        readtxt_2IMU(samples)
        visualize_2IMU()

def readtxt_2IMU(samples):
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

if __name__ == "__main__":
    file = "ear.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
        readTXT(file)
    else:
        readTXT(file)