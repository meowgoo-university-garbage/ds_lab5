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

def main():
    print("hello")

main()
