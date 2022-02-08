import glob
import os
import shutil
list = glob.glob(r"C:\Games\RRRsystem\Database\*\*\*\*\*\*_basic.txt")
list1 = glob.glob(r"C:\Games\RRRsystem\Database\*\*\*\*\*\*_S.txt")
f=open("matrix.txt","w")
f.write("Time blow ")
flag=0
for i in range(len(list)):
    read= open(list[i],"r")

    if flag == 0:
        flag=1
        count=0
        for l in read:
            count=count+1
            f.write(str("%.3f " % (0.5054*count))+" ")
        f.write("\n")
    filename=0
    # print(list1[i])
    j = open(list1[i],"r")
    for r in j:
        if not r.find("File Name"):
            filename= r.split()[2][0:16]
    j.close()
    flag_writ = 0
    f.write(filename + ' ')
    for line in read:
        if line.find("0.505") ==0:
            flag_writ=1
        if flag_writ==1:
            f.write(str("%.3f" % float(line.split()[1]))+" ")
    f.write("\n")

f.close()
