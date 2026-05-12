import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from collections import deque



MONTHS = [ "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec" ]


def load_minesweeper_data(path):
    stats = []
    dayMin = None
    dayMax = None

    with open(path, "r") as f:
        text = f.read()

        lines = text.splitlines()

        stat = {}

        for i, line in enumerate(lines):
            words = line.split(" ")

            if words[1] not in MONTHS:
                print("ERROR MONTH", line, i)

            dayIndex = datetime.strptime(words[0] + " " + words[1] + " " + " 2026", "%d %b %Y").timetuple().tm_yday

            if dayMin == None:
                dayMin = dayIndex

            if dayMax == None:
                dayMax = dayIndex

            if dayIndex < dayMin:
                dayMin = dayIndex

            if dayIndex > dayMax:
                dayMax = dayIndex

            stat["dayIndex"] = dayIndex
            stat["time"] = (int(words[2]) * 60) + (int(words[3]) * 1)

            stats.append(stat.copy())

    return stats, dayMin, dayMax
    
            

def remove_anomalies(source, p, nw, Q, strictValue = None):
    data = np.zeros(len(source))
    for i in range(len(data)):
        data[i] = source[i]

    
    _, c = least_squares(data, p)
    speed = c[1]



    
    for i in range(nw - 1, len(data)):
        avg_sum = 0
        avg_num = 0
        for j in range(i - nw + 1, i + 1):
            avg_num += 1
            avg_sum += data[j]
        if avg_num == 0:
            avg_num = 1
        avg = avg_sum / avg_num

        avg_num -= 1
        if avg_num == 0:
            avg_num = 1

        disp = 0
        for j in range(i - nw + 1, i + 1):
            disp += math.pow(avg - data[j], 2)
        disp /= avg_num

        dev = math.sqrt(disp)

        i1 = math.fabs(speed * math.sqrt(len(data)))
        i2 = math.fabs(Q * dev * speed * math.sqrt(nw))

        if i2 > i1 or (strictValue != None and data[i] == strictValue):
            data[i] = sample_least_squares(i, c)


    return data


def remove_anomalies_better(source, p, nw):
    data = np.zeros(len(source))
    for i in range(len(data)):
        data[i] = source[i]

    
    for i in range(nw - 1, len(data)):
        avg_sum = 0
        avg_num = 0
        for j in range(i - nw + 1, i + 1):
            avg_num += 1
            avg_sum += data[j]
        if avg_num == 0:
            avg_num = 1
        avg = avg_sum / avg_num

        disp = 0
        for j in range(i - nw + 1, i + 1):
            disp += math.pow(avg - data[j], 2)
        disp /= avg_num

        dev = math.sqrt(disp)

        for j in range(i - nw + 1, i + 1):
            z = (data[j] - avg) / dev
            if math.fabs(z) > 3:
                data[j] = avg

    return data







def file_parsing(URL, File_name, Data_name):
    d = pd.read_excel(File_name)
    for name, values in d[[Data_name]].items():
        pass
        # print(values)

    S_real = np.zeros((len(values)))
    for i in range(len(values)):
        S_real[i] = values[i]
    print('Джерело даних: ', URL)
    return S_real


def generate_anomaly_indexes(n, anomaly_count):
    anomaly_indexes = np.zeros((anomaly_count))
    for i in range(anomaly_count):
        anomaly_indexes[i] = math.ceil(np.random.randint(0, n))

    mS = np.median(anomaly_indexes)
    dS = np.var(anomaly_indexes)
    scvS = math.sqrt(dS)

    print("Generating anomalies")
    # print('Anomaly indexes: ', anomaly_indexes)
    print("\tAnomaly index expected: ", mS)
    print("\tAnomaly index dispersion: ", dS)
    print("\tAnomaly index deviation: ", scvS)

    return anomaly_indexes

def generate_measurement_noise(dm, dsig, n):
    # noise = np.random.normal(dm, dsig, n)
    noise = np.random.uniform(-0.1, 0.1, n)

    mS = np.median(noise)
    dS = np.var(noise)
    scvS = math.sqrt(dS)

    print("Generating noise")
    print("\tNoise expected: ", mS)
    print("\tNoise dispertion: ", dS)
    print("\tNoise deviation: ", scvS)

    # plt.hist(noise, bins=20, facecolor="blue", alpha=0.5)
    # plt.show()
    return noise



def calculate_noise_stats(data, Text):
    estimate, _ = least_squares(data, 5)
    # estimate = Model(len(data))

    noise = data - estimate[:, 0]

    mS = np.median(noise)
    dS = np.var(noise)
    scvS = math.sqrt(dS)

    print("Estimating noise: ", Text)
    print("\tNoise expected: ", mS)
    print("\tNoise dispertion: ", dS)
    print("\tNoise deviation: ", scvS)
    return

def sample_least_squares(x, C):
    p = np.zeros(len(C))
    for i in range(len(C)):
        p[i] = math.pow(x, i)
    r = np.dot(p, C)
    return r

def least_squares(data, p, increment = 0):
    p += 1
    n = len(data)
    Y = np.zeros((n, 1))
    F = np.zeros((n, p))
    FR = np.zeros((n + increment, p))
    for i in range(n):
        Y[i, 0] = float(data[i])
        for pp in range(p):
            F[i, pp] = math.pow(float(i), pp)
        # F[i, p - 1] = math.exp(-0.02 * (i - 300))

    for i in range(n + increment):
        for pp in range(p):
            FR[i, pp] = math.pow(float(i), pp)
        # FR[i, p - 1] = math.exp(-0.02 * (i - 300))

    FT = F.T
    C = np.linalg.inv(FT.dot(F)).dot(FT).dot(Y)

    result = FR.dot(C)
    C = C[:, 0]
    return result, C

def plot_diff(gs, Text):
    plt.clf()
    for g in gs:
        plt.plot(g)

    plt.ylabel(Text)
    plt.show()
    return


def Model(n):
    data = np.zeros((n))
    for i in range(n):
        data[i] = (0.0000005 * i*i)
        # data[i] = 3
    return data

def main():
    n = 10000
    noise_deviation = 5
    anomaly_count = int(n * 0.01)
    anomaly_deviation = 50



    # Pure trend
    trend_perfect = Model(n)


    # Trend with noise
    trend_noise = np.zeros((n))
    noise = generate_measurement_noise(0, noise_deviation, n)
    for i in range(n):
        trend_noise[i] = trend_perfect[i] + noise[i]

    # plot_diff(trend_perfect, trend_noise, "Model + Noise")
    # calculate_noise_stats(trend_noise, "Model + Noise")



    # Trend with noise and anomalies
    trend_noise_anomalies = np.zeros((n))
    for i in range(n):
        trend_noise_anomalies[i] = trend_noise[i]

    # anomaly_values = np.random.normal(0, anomaly_deviation, anomaly_count)
    anomaly_values = np.random.uniform(-20, 0, anomaly_count)
    anomaly_indexes = generate_anomaly_indexes(n, anomaly_count)
    for i in range(anomaly_count):
        k = int(anomaly_indexes[i])
        trend_noise_anomalies[k] += anomaly_values[i]

    # trend_restored, _ = least_squares(remove_anomalies(trend_noise_anomalies, 2, int(n / 10), 0.5), 2)
    # trend_restored = remove_anomalies(trend_noise_anomalies, 2, int(n / 20), 5)
    trend_restored = remove_anomalies_better(trend_noise_anomalies, 2, int(n / 20))
    trend_approx, _ = least_squares(trend_noise_anomalies, 2)
    trend_approx_restored, _ = least_squares(trend_restored, 2)
    plot_diff([trend_noise_anomalies, trend_restored, trend_perfect, trend_approx_restored, trend_approx], "Model + Noise + Anomalies")
    calculate_noise_stats(trend_noise_anomalies, "Model + Noise + Anomalies")




    MS_EXPONENT = 2
    MS_Q = 0.1


    ms_stats, ms_dayMin, ms_dayMax = load_minesweeper_data("minesweeper.txt")
    ms_stats.sort(key = lambda s: s["dayIndex"])

    ms_len = ms_dayMax - ms_dayMin + 1
    ms_len_half = int(ms_len / 2)

    ms_data_ravg = np.zeros(ms_len)
    for i in range(ms_len):
        temp_max = i
        temp_min = i - 15
        if temp_min < 0:
            temp_min = 0

        avg_num = 0
        avg_sum = 0
        for stat in ms_stats:
            m = stat["dayIndex"] - ms_dayMin
            if temp_min <= m and m <= temp_max:
                avg_num += 1
                avg_sum += float(stat["time"])

        if avg_num == 0:
            avg_num = 1

        ms_data_ravg[i] = avg_sum / avg_num



    ms_total_avg_sum = 0
    ms_total_avg_num = 0
    ms_data_avg = np.zeros(ms_len)
    for i in range(ms_len):
        for stat in ms_stats:
            if stat["dayIndex"] - ms_dayMin == i:
                ms_total_avg_num += 1
                ms_total_avg_sum += float(stat["time"])
        ms_data_avg[i] = ms_total_avg_sum / ms_total_avg_num






    ms_data_dmin = np.zeros(ms_len)
    for i in range(ms_len):
        m = None
        for stat in ms_stats:
            if stat["dayIndex"] - ms_dayMin == i:
                if m == None:
                    m = stat["time"]

                if stat["time"] < m:
                    m = stat["time"]

        if m == None:
            m = 0
        ms_data_dmin[i] = m


    ms_total_min = None
    ms_data_min = np.zeros(ms_len)
    for i in range(ms_len):
        for stat in ms_stats:
            if stat["dayIndex"] - ms_dayMin <= i:
                if ms_total_min == None:
                    ms_total_min = stat["time"]

                if stat["time"] < ms_total_min:
                    ms_total_min = stat["time"]

        ms_data_min[i] = ms_total_min


    ms_data_dcount = np.zeros(ms_len)
    for i in range(ms_len):
        n = 0
        for stat in ms_stats:
            if stat["dayIndex"] - ms_dayMin == i:
                n += 1

        ms_data_dcount[i] = n


    ms_total_count = 0
    ms_data_count = np.zeros(ms_len)
    for i in range(ms_len):
        for stat in ms_stats:
            if stat["dayIndex"] - ms_dayMin == i:
                ms_total_count += 1
        ms_data_count[i] = ms_total_count




    # Analyzing real data
    ms_data_ravg_estimate, _ = least_squares(ms_data_ravg, MS_EXPONENT, ms_len_half)
    plot_diff([ms_data_ravg_estimate, ms_data_ravg], "Minesweeper rolling average")
    calculate_noise_stats(ms_data_ravg, "Minesweeper rolling average")



    ms_data_avg_estimate, _ = least_squares(ms_data_avg, MS_EXPONENT, ms_len_half)
    plot_diff([ms_data_avg_estimate, ms_data_avg], "Minesweeper total average")
    calculate_noise_stats(ms_data_avg, "Minesweeper total average")



    # ms_data_dmin_removed = remove_anomalies(ms_data_dmin, MS_EXPONENT, 15, MS_Q, strictValue = 0)
    ms_data_dmin_removed = remove_anomalies_better(ms_data_dmin, MS_EXPONENT, 15)
    ms_data_dmin_estimate, _ = least_squares(ms_data_dmin_removed, MS_EXPONENT, ms_len_half)
    plot_diff([ms_data_dmin_estimate, ms_data_dmin, ms_data_dmin_removed], "Minesweeper min per day")
    calculate_noise_stats(ms_data_dmin, "Minesweeper min per day")



    ms_data_min_estimate, _ = least_squares(ms_data_min, MS_EXPONENT, ms_len_half)
    plot_diff([ms_data_min_estimate, ms_data_min], "Minesweeper min total")
    calculate_noise_stats(ms_data_min, "Minesweeper min total")



    ms_data_dcount_estimate, _ = least_squares(ms_data_dcount, MS_EXPONENT, ms_len_half)
    plot_diff([ms_data_dcount_estimate, ms_data_dcount], "Minesweeper daily count")
    calculate_noise_stats(ms_data_dcount, "Minesweeper daily count")



    ms_data_count_estimate, _ = least_squares(ms_data_count, MS_EXPONENT, ms_len_half)
    plot_diff([ms_data_count_estimate, ms_data_count], "Minesweeper total count")
    calculate_noise_stats(ms_data_count, "Minesweeper total count")

main()

