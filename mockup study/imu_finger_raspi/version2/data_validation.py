import os, sys
import mediapipe as mp
import cv2
import numpy as np


def cluster(iterable, thre):
    prev = None
    clusters = []
    group = []
    for item in iterable:
        if prev is None or item - prev <= thre:
            group.append(item)
        else:
            clusters.append(group)
            group = [item]
        prev = item
    if group:
        clusters.append(group)

    return clusters


def find_clusters(flags, CLIP_CONFIG):

    length = len(flags)

    flags = np.array(flags)

    ones = np.argwhere(flags == 1).squeeze(1)

    # if distance is less than 7 frames away, then consider it as same cluster
    same_cluster = CLIP_CONFIG['same_cluster']

    clusters = cluster(ones, same_cluster)

    # print(clusters)

    files = []

    cluster_len_thre = CLIP_CONFIG['cluster_len_thre']

    # if cluster is no longer than thre, then drop it.
    for l in clusters:
        if len(l) > cluster_len_thre:
            files.append((l[0], l[-1]))

    min_idx = min([i[0] for i in files])
    max_idx = max([i[1] for i in files])

    # print(max_idx, min_idx, max_idx-min_idx, length)

    return (max_idx - min_idx)*1.0 / length


def video_checker(video_path, threshold_for_video_quality=0.3):

    CLIP_CONFIG = {'same_cluster': 15,
            'cluster_len_thre': 15,
            'fps': 30.0,
            'extra_s': 10,
            'extra_e': 20,
            }

    HAND_CONFIG = {'comp': 1,
            'min_det': 0.3,
            'min_tra': 0.3,
            }

    POSE_CONFIG = {'comp': 1,
            'min_det': 0.3,
            'min_tra': 0.3,
            }

    mp_hands = mp.solutions.hands
    mp_pose = mp.solutions.pose

    hands = mp_hands.Hands(
          model_complexity=HAND_CONFIG['comp'],
          min_detection_confidence=HAND_CONFIG['min_det'],
          min_tracking_confidence=HAND_CONFIG['min_tra'])



    pose = mp_pose.Pose(
        model_complexity=POSE_CONFIG['comp'],
        min_detection_confidence=POSE_CONFIG['min_det'],
        min_tracking_confidence=POSE_CONFIG['min_tra'])


    flags = []

    cap = cv2.VideoCapture(video_path)

    success, image = cap.read()

    while(success):

        if not success:
            print("Ignoring empty camera frame.")
            break

        image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results_hand = hands.process(image2)
        results_pose = pose.process(image2)

        if results_hand.multi_hand_landmarks:
            flags.append(1)
        else:
            flags.append(0)

        success, image = cap.read()

    percentage = find_clusters(flags, CLIP_CONFIG)

    if percentage < threshold_for_video_quality:
        print('video {} not good for extracting keypoints'.format(video_path))
        return False
    else:
        print('video {} passed!'.format(video_path))
        return True

def one_imu_checker(imu_path):
    portion = 0.1 # if {portion%} of a column is zeros, then go see if hardware has issues

    imu = np.loadtxt(imu_path, delimiter=',')
    imu = imu[:-1] # ignore timestamps

    def zero_checker(imu_zeros, thre ):

        same_cluster = 7 # if distance is less than 7 frames away, then consider it as same cluster
        clusters = cluster(imu_zeros, same_cluster)
        # print(thre, clusters, map(lambda x: len(x) >= thre, clusters))

        hasIssue = any(map(lambda x: len(x) >= thre, clusters))
        return hasIssue

    for i in range(imu.shape[1]):
        data = imu[:, i]

        imu_zeros = np.argwhere(data == 0).squeeze(1)

        if len(imu_zeros) >= imu.shape[0]*portion:
            hasIssue = zero_checker(imu_zeros, imu.shape[0]*portion)
            if hasIssue:
                print('dim {} has continue zeros'.format(i))
                return False
        else:
            continue


    print('imu file {} passed!'.format(imu_path))
    return True

def hand_imu_fre_checker(left_imu_path,right_imu_path,left_freq,right_freq,left_total,right_total,fre_threshold = 61,diff_total_threshold = 40):
    if left_freq < fre_threshold:
        print('imu file {} passed!'.format(left_imu_path))
        print('imu file {} failed!'.format(left_imu_path))
        return False

    if right_freq < fre_threshold:
        print('imu file {} passed!'.format(right_imu_path))
        return False

    if abs(right_total-left_total) > diff_total_threshold:
        print("Difference of total sampling number is bigger than {}".format(fre_threshold))
        print('imu file {} failed!'.format(right_imu_path))
        return False

    # if abs(right_total-left_total) > diff_total_threshold:
    #     print("Difference of total sampling number is bigger than {}".format(diff_total_threshold))
    #     return False

    one_imu_checker(left_imu_path)
    one_imu_checker(right_imu_path)
    return True



if __name__ =='__main__':
    video_checker('bob_47.mp4')
    # video_checker('/Users/taitinglu/Documents/GitHub/Ring/mockup study/experiment result/bob/videos/bob_54_section1.mp4')
    # one_imu_checker('/Users/taitinglu/Documents/GitHub/Ring/mockup study/experiment result/jack/left#1/jack_84_section2_left#1.txt')
    # hand_imu_fre_checker('./left_0000.txt','./left_0000.txt',0.86,0.87,860,870)
    # hand_imu_fre_checker('./right.txt','./left_0000.txt',0.86,0.87,860,870)






