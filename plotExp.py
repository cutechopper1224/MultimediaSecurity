import matplotlib.pyplot as plt
import numpy as np

#buildindex

x = [1000, 2000, 3000, 4000, 5000] 
UDMRS = [4.347467, 8.645039, 12.790471, 17.792289, 22.254384]
BDMRS = [13.651298, 26.120732, 38.171893, 52.255318, 62.007294]
EDMRS = [17.172533, 29.983388, 41.673500, 55.781504, 67.072613]
line1, = plt.plot(x, UDMRS, 'r--', label='UDMRS')
line2, = plt.plot(x, BDMRS, 'b:', label='BDMRS')
line3, = plt.plot(x, EDMRS, 'g-', label='EDMRS')

plt.xlabel('Number of Documents')
plt.ylabel('Time(s)')
plt.legend(handles = [line1, line2, line3], loc='upper left')
plt.xticks(x)
plt.title('Building Index Elapsed Time')
plt.savefig("result/BuildIndex.png")
plt.cla()

#generate trapdoor
BDMRS = [2.335814, 2.002968, 2.191845, 2.004050, 2.308579]
EDMRS = [2.778903, 3.042751, 2.753514, 3.152221, 3.209529]

line1, = plt.plot(x, BDMRS, 'b:', label='BDMRS')
line2, = plt.plot(x, EDMRS, 'g-', label='EDMRS')

plt.xlabel('Number of Documents')
plt.ylabel('Time(s)')
plt.legend(handles = [line1, line2], loc='upper left')
plt.xticks(x)
plt.title('Building Trapdoor Elapsed Time (5 keywords)')
plt.savefig("result/GenTrapdoor.png")
plt.cla()

#Search Time
UDMRS_s = [0.8, 2.750081, 2.5341384, 3.412564, 4.303046]
BDMRS_s = [1.5, 3.824766, 5.663200, 6.456815, 7.939308]
EDMRS_s = [1.913705, 4.761681, 5.170001, 6.881787, 8.436392]
line1, = plt.plot(x, UDMRS_s, 'r--', label='UDMRS')
line2, = plt.plot(x, BDMRS_s, 'b:', label='BDMRS')
line3, = plt.plot(x, EDMRS_s, 'g-', label='EDMRS')

plt.xlabel('Number of Documents')
plt.ylabel('Time(s)')
plt.legend(handles = [line1, line2, line3], loc='upper left')
plt.xticks(x)
plt.title('Searching Elapsed Time (100 results)')
plt.savefig("result/SearchTime.png")
plt.cla()

#Total Search Time
UDMRS_t = UDMRS_s
BDMRS_t = [BDMRS[i] + BDMRS_s[i] for i in range(5)]
EDMRS_t = [EDMRS[i] + EDMRS_s[i] for i in range(5)]
line1, = plt.plot(x, UDMRS_t, 'r--', label='UDMRS')
line2, = plt.plot(x, BDMRS_t, 'b:', label='BDMRS')
line3, = plt.plot(x, EDMRS_t, 'g-', label='EDMRS')

plt.xlabel('Number of Documents')
plt.ylabel('Time(s)')
plt.legend(handles = [line1, line2, line3], loc='upper left')
plt.xticks(x)
plt.title('Total Searching Time')
plt.savefig("result/TotalSearchTime.png")
plt.cla()