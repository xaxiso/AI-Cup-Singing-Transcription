import json
import sys
import glob
import os.path
import statistics
import numpy as np
import matplotlib.pyplot as plt

predict_list  = []

# x_min, x_max, y_min, y_max = 0, 7, 54, 74
def pvPlot1(pitch, time):
    plt.plot(time, pitch, 'r.')
    plt.axis([0, 220, 54, 74])
    plt.show()

def pvPlot2(sample_pitch, sample_time):
    plt.plot(sample_time, sample_pitch, 'r.')
    plt.axis([0, 7, 54, 74])
    plt.show()

def pvPlay(is_value, sample_time):
    plt.bar(sample_time, is_value, width=0.05)
    plt.show()

def notePlot(start_t: list, end_t: list, note: list):
    for (s, e, n) in zip(start_t, end_t, note):
        plt.plot([float(s), float(e)], [float(n), float(n)], color='b')
        plt.plot(s, n, 'b>')
    plt.axis([0, 7, 54, 74])
    plt.show()

def pv2note(pitch, time, threshold=1.5):
    assert len(pitch)==len(time) and threshold>0
    segement_list = []
    base_val = 0.0
    start_time = 0.0
    for val, now_time in zip(pitch, time):
        if len(segement_list) == 0 and val != 0:
            segement_list.append(val)
            base_val = val
            start_time = now_time
        elif abs(val - base_val) < threshold and val != 0:
            segement_list.append(val)
        elif val != 0:
            predict_list.append([start_time, now_time, np.median(segement_list)])
            start_time = now_time
            segement_list = [val]
            base_val = val
        else:
            if len(segement_list) > 0:
                predict_list.append([start_time, now_time, np.median(segement_list)])
                segement_list = []
    if len(segement_list) > 0:
        predict_list.append([start_time, now_time, np.median(segement_list)])

    # print(predict_list)


if __name__ == "__main__":

    allFiles = glob.glob('./MIR-ST500/*/*_vocal.json')
    id = 1

    fp = open("all_vocal_output.txt", "a+") #adds to the file
    fp.truncate(0)

    for file in allFiles:
        with open(file , 'r') as reader:
            jf = json.loads(reader.read())

        print(file)

        time = np.zeros(len(jf))
        for i in range(len(jf)):
            time[i] = jf[i][0]

        pitch = np.zeros(len(jf))
        for i in range(len(jf)):
            pitch[i] = jf[i][1]

        pv2note(pitch, time)
        

        fp.write('\n'.join(str(id)))
        id += 1
        fp.write('\n'.join(str(i) for i in predict_list))

    fp.close()

    # start = 0
    # total = []
    # track = 0

    # for i in range(len(jf)):
    #     if jf[i][1] == 0.0:
    #         track += 1
    #         continue
    #     elif (abs(jf[i][1]-jf[i-1][1]) < 1.5) or (jf[i][1] > 0 and jf[i-1][1] == 0): #or compare with abs(start-jf[i][1])
    #         if start == 0:
    #             start = jf[i][0]

    #         if jf[i-2][1] == 0.0: # because this elif would not pass immediately
    #             total.append(jf[i-1][1])

    #         total.append(jf[i][1])
    #     elif abs(jf[i][1]-jf[i-1][1]) >= 1.5:
    #         med = np.median(total)
    #         print(i, med)
    #         # med = int(round(med))
    #         # fp.write("%d %d %d\n" % (start, jf[i][0], med))
    #         start = 0
    #         track = 0
    #         total = []

    #         start = jf[i][0]
    #         total.append(jf[i][1])
    #     else:
    #         med = np.median(total)
    #         print(i, med)
    #         # med = int(round(med))
    #         # fp.write("%d %d %d\n" % (start, jf[i][0], med))
    #         start = 0
    #         track = 0
    #         total = []

    # print(len(jf))


    

    # with open('./MIR-ST500/6/6_feature.json' , 'r') as reader:
    #     jf = json.loads(reader.read())

    # pitch = np.array(jf['vocal_pitch'])
    # print(jf['vocal_pitch'])
    # time = np.array(jf['time'])
    # print(jf['time'])
    # pvPlot1(pitch, time)

    # index = (time >= 27) & (time <= 33.5)
    # sample_pitch = pitch[index]
    # sample_time = time[index]-27
    # pvPlot2(sample_pitch, sample_time)

    # is_value = [ (v) and 1 or 0 for v in sample_pitch]
    # pvPlay(is_value, sample_time)
    
    # threshold = 1.5
    # segement_list = []
    # answer_list = []
    # base_val = None
    # start_time = None
    # for val, now_time in zip(sample_pitch, sample_time):
    #     if len(segement_list) == 0 and val != 0:
    #         segement_list.append(val)
    #         base_val = val
    #         start_time = now_time
    #     elif abs(val - base_val) < threshold and val != 0:
    #         segement_list.append(val)
    #     elif val != 0:
    #         answer_list.append((start_time, now_time, np.median(segement_list)))
    #         start_time = now_time
    #         segement_list = [val]
    #         base_val = val
    #     else:
    #         if len(segement_list) > 0:
    #             answer_list.append((start_time, now_time, np.median(segement_list)))
    #             segement_list = []
    # if len(segement_list) > 0:
    #     answer_list.append((start_time, now_time, np.median(segement_list)))

    # for i in answer_list:
    #     print(i)
    # for i in sample_pitch:
    #     print(i)
    # plt.plot(sample_time, sample_pitch, 'r.')
    # for (s, e, p) in answer_list:
    #     plt.plot([float(s), float(e)], [float(p), float(p)], color='b')
    #     plt.plot(s, p, 'b>')
    #     print((float(s), float(e), float(p)))
    # plt.axis([0, 7, 54, 74])
    # plt.show()

    # with open('./MIR-ST500/6/6_groundtruth.txt', 'r') as f:
    #     gt = [line.strip().split() for line in f.readlines()]
    #     gt = np.array([[float(i) for i in vals] for vals in gt])

    # index = (gt[:,0] >= 27) & (gt[:,1] <= 33.5)

    # # plt.rcParams['lines.linewidth']=2
    # for i in gt[index]:
    #     # plt.axhline(i[2], i[0], i[1], color='b')
    #     plt.plot([i[0], i[1]], [i[2], i[2]], color='b')
    #     plt.plot(i[0], i[2], 'b>')
    #     # print(i)
    # plt.axis([27, 33.5, 54, 74])
    # plt.show()