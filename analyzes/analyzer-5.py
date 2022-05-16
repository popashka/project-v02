import pandas as pd
import re
from datetime import datetime, date, time
import math
from matplotlib import pyplot

df = pd.read_csv ('mdrn.csv')
print(df)

p1 = df.iat[0, 2]

print(df.shape[0])


### Приводим данные в читаемый вид

for i in range(df.shape[0]):
    p1 = df.iat[i, 2]
    p1 = p1.replace(".", "")
    p1 = p1.replace(",", ".")
    df.iat[i, 2] = p1

    p1 = df.iat[i, 4]
    p1 = p1.replace(",", ".")
    df.iat[i, 4] = p1


### Заменяем рубли на доллары, чтобы сравнивать в одной валюте

pmsc = []
pldn= []
ppit = []

for i in range(df.shape[0]):
    p1 = float(df.iat[i, 2])

    change = float(df.iat[i, 4])

    p1 /= change
    df.iat[i, 2] = p1
    pmsc.append(df.iat[i, 2])
    pldn.append(df.iat[i, 1])
    ppit.append(df.iat[i, 0])

pyplot.plot(pmsc, 'b', label='msc')
pyplot.plot(pldn, 'r', label='ldn')
pyplot.plot(ppit, 'g', label='pit')
#pyplot.ylim(ymax = 40, ymin = -20)
pyplot.title('mdrn prices')
pyplot.legend()
pyplot.show()

print(df)

df.to_csv('mdrn-ann.csv', mode='a', index=False, header=False)

### Будем насчитывать волатильность каждой биржы по каждому дню

msc = []
ldn = []
pit = []

mecmsc = []
mecldn = []
mecpit = []

admsc = []
adldn = []
adpit = []

mnmsc = mxmsc = df.iat[0, 2]
mnldn = mxldn = df.iat[0, 1]
mnpit = mxpit = df.iat[0, 0]
was = int(df.iat[0, 3][8:10])

lmn1 = lmx1 = mnmsc
lmn2 = lmx2 = mnldn
lmn3 = lmx3 = mnpit

dif1 = 0
dif2 = 0
dif3 = 0

cnt = 1

for i in range(df.shape[0]):
    now = int(df.iat[i, 3][8:10])
    if (was == now):
        mnmsc = min(mnmsc, float(df.iat[i, 2]))
        mxmsc = max(mxmsc, float(df.iat[i, 2]))
        #lmn1 = min(lmn1, float(df.iat[i, 2]))
        #lmx1 = max(lmx1, float(df.iat[i, 2]))
        admsc.append(abs(float(df.iat[i, 2]) / float(df.iat[i - 1, 2])))

        mnldn = min(mnldn, float(df.iat[i, 1]))
        mxldn = max(mxldn, float(df.iat[i, 1]))
        #lmn2 = min(lmn2, float(df.iat[i, 1]))
        #lmx2 = max(lmx2, float(df.iat[i, 1]))
        adldn.append(abs(float(df.iat[i, 1]) / float(df.iat[i - 1, 1])))

        mnpit = min(mnpit, float(df.iat[i, 0]))
        mxpit = max(mxpit, float(df.iat[i, 0]))
        #lmn3 = min(lmn3, float(df.iat[i, 0]))
        #lmx3 = max(lmx3, float(df.iat[i, 0]))
        adpit.append(abs(float(df.iat[i, 0]) / float(df.iat[i - 1, 0])))
    else :
        was = now
        msc.append((mxmsc - mnmsc) )
        ldn.append((mxldn - mnldn) )
        pit.append((mxpit - mnpit) )

        mnmsc = mxmsc = df.iat[i, 2]
        mnldn = mxldn = df.iat[i, 1]
        mnpit = mxpit = df.iat[i, 0]
        lmn1 = lmx1 = mnmsc
        lmn2 = lmx2 = mnldn
        lmn3 = lmx3 = mnpit
        cnt = 0

    cnt += 1

    dif1 = dif1 + (max(df.iat[i, 2], df.iat[i, 1]) / min(df.iat[i, 2], df.iat[i, 1]))
    dif2 = dif2 + (max(df.iat[i, 2], df.iat[i, 0]) / min(df.iat[i, 2], df.iat[i, 0]))
    dif3 = dif3 + (max(df.iat[i, 1], df.iat[i, 0]) / min(df.iat[i, 1], df.iat[i, 0]))

    if (cnt == 5):
        d11 = d12 = 1
        if (admsc[len(admsc) - 1] != 0) :
            d12 = math.log(float(admsc[len(admsc) - 1]))

        d11 = math.log(df.iat[i, 2] / lmn1)

        if (d12 != 0):
            mecmsc.append(d11 / (4 * d12))
        else :
            mecmsc.append(1)

        d11 = d12 = 1
        if (adldn[len(adldn) - 1] != 0) :
            d12 = math.log(float(adldn[len(adldn) - 1]))

        d11 = math.log(df.iat[i, 1] / lmn2)

        if (d12 != 0):
            mecldn.append(d11 / (4 * d12))
        else :
            mecldn.append(1)

        d11 = d12 = 1
        if (adpit[len(adpit) - 1] != 0) :
            d12 = math.log(float(adpit[len(adpit) - 1]))

        d11 = math.log(df.iat[i, 0] / lmn3)

        if (d12 != 0):
            mecpit.append(d11 / (4 * d12))
        else :
            mecpit.append(1)

        #mecpit.append(math.log(lmx3 - lmn3) / (5 * math.log(float(adpit[len(adpit) - 1]))))
        cnt = 0



msc.append((mxmsc - mnmsc))
ldn.append((mxldn - mnldn))
pit.append((mxpit - mnpit))

dif1 /= df.shape[0]
dif2 /= df.shape[0]
dif3 /= df.shape[0]

print("Differences are")
print("msc-ldn ")
print(dif1)
print("msc-pit ")
print(dif2)
print("ldn-pit ")
print(dif3)

d = {'msc': msc, 'ldn': ldn, 'pit': pit}

df2 = pd.DataFrame(data=d)
df2.to_csv('mdrn-an.csv')

d2 = {'msc': mecmsc, 'ldn': mecldn, 'pit': mecpit}
df3 = pd.DataFrame(data=d2)
df3.to_csv('mdrn-mec.csv')

avm1 = 0
avm2 = 0
avm3 = 0

for i in range(len(mecmsc)):
    avm1 += (mecmsc[i])
    avm2 += (mecldn[i])
    avm3 += (mecpit[i])

avm1 /= len(mecmsc)
avm2 /= len(mecldn)
avm3 /= len(mecpit)

print("Avengers")
print(avm1)
print(avm2)
print(avm3)

#pyplot.plot(admsc, 'bo', label='msc deltas')
#pyplot.plot(adldn, 'r', label='ldn deltas')
#pyplot.plot(adpit, 'limegreen', label='pit deltas')
#pyplot.ylim(ymax = 1.02, ymin = 0.98)
#pyplot.title('moderna deltas')
#pyplot.legend()
#pyplot.show()

#pyplot.plot(msc, 'bo', label='msc volatil')
#pyplot.plot(ldn, 'ro', label='ldn volatil')
#pyplot.plot(pit, 'go', label='pit volatil')
#pyplot.ylim(ymax = 1.02, ymin = 0.98)
#pyplot.title('moderna volatil')
#pyplot.legend()
#pyplot.show()

#pyplot.plot(mecmsc, 'b', label='msc mec')
#pyplot.plot(mecldn, 'r', label='ldn mec')
#pyplot.plot(mecpit, 'g', label='pit mec')
#pyplot.ylim(ymax = 10, ymin = -10)
#pyplot.title('mdrn mec')
#pyplot.legend()
#pyplot.show()



d3 = {'msc': admsc, 'ldn': adldn, 'pit': adpit}
df4 = pd.DataFrame(data = d3)
df4.to_csv('tcs-deltas.csv')

avmsc = 0
avldn = 0
avpit = 0

for i in range(len(msc)):
    avmsc += msc[i]
    avldn += ldn[i]
    avpit += pit[i]

avmsc /= len(msc)
avldn /= len(ldn)
avpit /= len(pit)

print(avmsc)
print(avldn)
print(avpit)
