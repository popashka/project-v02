import pandas as pd
import re
from datetime import datetime, date, time
import math
from matplotlib import pyplot
import numpy as np


df = pd.read_csv ('pars.csv')
print(df)

for i in range(df.shape[0]):
    p1 = float(df.iat[i, 6])
    p2 = float(df.iat[i, 7])
    p3 = float(df.iat[i, 8])
    p1 *= 0.96
    p2 *= 0.96
    p3 *= 0.96
    df.iat[i, 6] = p1
    df.iat[i, 7] = p2
    df.iat[i, 8] = p3
    df.iat[i, 2] = float( (float(df.iat[i, 0]) + float(df.iat[i, 1])) / 2)

spred1 = []
spred2 = []
spred3 = []
spred4 = []

for i in range(df.shape[0]):
    spred1.append(float(df.iat[i, 1]) - float(df.iat[i, 0]))
    spred2.append(float(df.iat[i, 4]) - float(df.iat[i, 3]))
    spred3.append(float(df.iat[i, 7]) - float(df.iat[i, 6]))
    spred4.append(float(df.iat[i, 10] - float(df.iat[i, 9])))


#pyplot.plot(spred1, 'b', label='Xetra Spread')
#pyplot.plot(spred2, 'r', label='Stut Spread')
#pyplot.plot(spred3, 'g', label='Bx Spread')
#pyplot.plot(spred4, 'y', label='Six Spread')
#pyplot.ylim(ymax = 0.07, ymin = 0)
#pyplot.title('Spread Bitcoin')
#pyplot.legend()
#pyplot.show()

dif1 = []
dif2 = []
dif3 = []

p1 = []
p2 = []
p3 = []
p4 = []

for i in range(df.shape[0]):
    p1.append(df.iat[i, 2])
    p2.append(df.iat[i, 5])
    p3.append(df.iat[i, 8])
    p4.append(df.iat[i, 11])
    dif1.append(max(float(df.iat[i, 2]), float(df.iat[i, 5])) / min(float(df.iat[i, 2]), float(df.iat[i, 5])))
    dif2.append(max(float(df.iat[i, 5]), float(df.iat[i, 8])) / min(float(df.iat[i, 5]), float(df.iat[i, 8])))
    dif3.append(max(float(df.iat[i, 8]), float(df.iat[i, 11])) / min(float(df.iat[i, 8]), float(df.iat[i, 11])))

pyplot.plot(p1, 'b', label='Xetra')
pyplot.plot(p2, 'r', label='Stut')
pyplot.plot(p3, 'g', label='Bx')
pyplot.plot(p4, 'y', label='Six')
#pyplot.ylim(ymax = 0.07, ymin = 0)
pyplot.title('prices bit')
pyplot.legend()
pyplot.show()


#pyplot.plot(dif1, 'b', label='Xetra Stut dif')
#pyplot.plot(dif2, 'r', label='Stut Bx dif')
#pyplot.plot(dif3, 'g', label='Bx Six dif')
#pyplot.ylim(ymax = 0.07, ymin = 0)
#pyplot.title('bit ratios')
#pyplot.legend()
#pyplot.show()

mn1 = mx1 = df.iat[0, 2]
mn2 = mx2 = df.iat[0, 5]
mn3 = mx3 = df.iat[0, 8]
mn4 = mx4 = df.iat[0, 11]
was = int(df.iat[0, 12][8:10])

l1 = mn1
l2 = mn2
l3 = mn3
l4 = mn4

vol1 = []
vol2 = []
vol3 = []
vol4 = []

ad1 = []
ad2 = []
ad3 = []
ad4 = []

cnt = 0

mec1 = []
mec2 = []
mec3 = []
mec4 = []

for i in range(df.shape[0]):
    now = df.iat[i, 12][8:10]

    if (now == was):
        mn1 = min(mn1, float(df.iat[i, 2]))
        mx1 = max(mx1, float(df.iat[i, 2]))
        ad1.append(float(df.iat[i, 2]) / float(df.iat[i - 1, 2]))

        mn2 = min(mn2, float(df.iat[i, 5]))
        mx2 = max(mx2, float(df.iat[i, 5]))
        ad2.append(float(df.iat[i, 5]) / float(df.iat[i - 1, 5]))


        mn3 = min(mn3, float(df.iat[i, 8]))
        mx3 = max(mx3, float(df.iat[i, 8]))
        ad3.append(float(df.iat[i, 8]) / float(df.iat[i - 1, 8]))


        mn4 = min(mn4, float(df.iat[i, 11]))
        mx4 = max(mx4, float(df.iat[i, 11]))
        ad4.append(float(df.iat[i, 11]) / float(df.iat[i - 1, 11]))

    else :
        vol1.append(mx1 - mn1)
        vol2.append(mx2 - mn2)
        vol3.append(mx3 - mn3)
        vol4.append(mx4 - mn4)
        cnt = 0
        was = now
        l1 = mn1 = mx1 = df.iat[i, 2]
        l2 = mn2 = mx2 = df.iat[i, 5]
        l3 = mn3 = mx3 = df.iat[i, 8]
        l4 = mn4 = mx4 = df.iat[i, 11]

    cnt += 1

    if (cnt == 5):
        if (l1 != 0 and math.log(ad1[len(ad1) - 1]) != 0):
            mec1.append(math.log(df.iat[i, 2] / l1) / (4 * math.log(ad1[len(ad1) - 1])))
        else:
            mec1.append(1)

        if (l2 != 0 and math.log(ad2[len(ad2) - 1]) != 0):
            mec2.append(math.log(df.iat[i, 5] / l2) / (4 * math.log(ad2[len(ad1) - 1])))
        else:
            mec2.append(1)

        if (l3 != 0 and math.log(ad3[len(ad3) - 1]) != 0):
            mec3.append(math.log(df.iat[i, 8] / l3) / (4 * math.log(ad3[len(ad1) - 1])))
        else:
            mec3.append(1)

        if (l4 != 0 and math.log(ad4[len(ad4) - 1]) != 0):
            mec4.append(math.log(df.iat[i, 2] / l4) / (4 * math.log(ad4[len(ad1) - 1])))
        else:
            mec4.append(1)

        cnt = 0





#pyplot.plot(vol1, 'b', label='Xetra Volatility')
#pyplot.plot(vol2, 'r', label='Stut Volatility')
#pyplot.plot(vol3, 'g', label='Bx Volatility')
#pyplot.plot(vol4, 'y', label='Six Volatility')
#pyplot.ylim(ymax = 0.07, ymin = 0)
#pyplot.title('Bit Volatility')
#pyplot.legend()
#pyplot.show()

#pyplot.plot(ad1, 'b', label='Xetra Delta')
#pyplot.plot(ad2, 'r', label='Stut Delta')
#pyplot.plot(ad3, 'g', label='Bx Delta')
#pyplot.plot(ad4, 'y', label='Six Delta')
#pyplot.ylim(ymax = 1.01, ymin = 0.99)
#pyplot.title('Bit Deltas')
#pyplot.legend()
#pyplot.show()


#pyplot.plot(mec1, 'b', label='Xetra Mec')
#pyplot.plot(mec2, 'r', label='Stut Mec')
#pyplot.plot(mec3, 'g', label='Bx Mec')
#pyplot.plot(mec4, 'y', label='Six Mec')
#pyplot.title('Bit Mec')
#pyplot.ylim(ymax = 50, ymin = -30)
#pyplot.legend()
#pyplot.show()