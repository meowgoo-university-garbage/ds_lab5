import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import cv2



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

def main():
    stats, dayMin, dayMax = load_minesweeper_data("./minesweeper.txt")

    statsRaw = []
    for s in stats:
        statsRaw.append((float(s["dayIndex"]), float(s["time"])))
    statsRaw = np.array(statsRaw, dtype = np.float32)

    mins = statsRaw.min(axis=0)
    maxs = statsRaw.max(axis=0)

    statsNorm = (statsRaw - mins) / (maxs - mins)
    # statsNorm = statsRaw



    k = 7
    compactness, labels, centers = cv2.kmeans(statsNorm, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2), 10, cv2.KMEANS_PP_CENTERS)
    labels = labels.flatten()



    plt.figure(figsize=(6, 6))

    for i in range(k):
        cluster = statsRaw[labels == i]
        plt.scatter(cluster[:, 0], cluster[:, 1])

    plt.title("minesweeper clusterized")
    plt.xlabel("day")
    plt.ylabel("game time")
    plt.legend()
    plt.grid(True)

    plt.show()

main()
