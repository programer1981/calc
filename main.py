import glob
import os
import constant as c
from datetime import datetime
Datapath = r"C:\Games\RRRsystem\Database"
Tempfile_path=r"C:\Games\RRRsystem\tempFiles"
step=0.5054


def getgata(new,base,id):
    new_file = open(new,"r")
    base_file = open(base, "r")
    date=0
    res=0
    int=0
    avg=0
    mod=0
    for s in new_file:
        if not s.find("Date"):
            date=s
        elif not s.find("Spatial Resolution"):
            res=s
        elif not s.find("Sampling Interval"):
            int=s
        elif not s.find("Averaging"):
            avg=s
        elif not s.find("Sensor configuration"):
            mod=s

    string_data_new=str("New file "+date+res+int+avg+mod)
    date=0
    res=0
    int=0
    avg=0
    for s in base_file:
        if not s.find("Date"):
            date=s
        elif not s.find("Spatial Resolution"):
            res=s
        elif not s.find("Sampling Interval"):
            int=s
        elif not s.find("Averaging"):
            avg=s
        elif not s.find("Sensor configuration"):
            mod=s

    full_hed=str("ID line " +id + "\n" + string_data_new+"\n"+"Base file "+date+res+int+avg+mod)

    new_file.close()
    base_file.close()
    return full_hed

def temp_correction(t_data,s_data,K_L,B_L,K_H,B_H,str_point): # температурная корекция

    e = []
    calib_str = []
    for i in range(len(t_data)):
        if t_data[i] > str_point:
            calib_str.append(float(K_H * t_data[i] + B_H))
        else:
            calib_str.append(float(K_L * t_data[i] + B_L))
    if len(calib_str) >= len(s_data):
        for i in range(len(s_data) - 1):
            e.append((float(s_data[i]) - calib_str[i]) * 1000)
    else:
        for i in range(len(calib_str)):
            e.append((float(s_data[i]) - calib_str[i]) * 1000)

    return e
    #возвращает чистые стрейны


def temperatuer_count(t_new1,t_B_L,t_B_H,t_K_H,t_K_L,temG_point): # Counting temperature

    ret=[]
    for i in range(len(t_new1)):
        if t_new1[i] > temG_point:
            ret.append(float(t_new1[i]-t_B_H)/t_K_H)
        else:
            ret.append((float(t_new1[i] - t_B_L) / t_K_L))
    return ret




def readFile_f_tunnel(name):
    data=[]
    flag=0
    file = open(name, "r")
    for line in file:
        if not line.find("[DATA]"):
            flag =1
        if flag==1 and not line == "\n":
            try:
                data.append(line)
            except:
                print("")
    file.close()
    return (data)



def board_arr(data,start,stop):
    temp_a=[]
    i = 0
    for i in range(len(data)):
        if data[i].find(start) == 0:
            while(float(data[i].split()[0]) <= float(stop)):
                temp_a.append(float(data[i].split()[1]))
                i=i+1

    return(temp_a)

def getname(id):
    now = datetime.now()
    year = now.strftime("%Y")
    m = now.strftime("%m")
    day = now.strftime("%d")
    hour = now.strftime("%H-%M")
    return str(id+"_"+year+"_"+m+"_"+day+"_"+hour)

def export(data,path,id,step):
    dis=0
    name=getname(id)
    f=open(path+"/"+name+"_Temp.txt", "w")
    for i in data:
        dis=dis+1
        f.write(str('%.3f' % (step*dis))+" "+str(i)+'\n')
    f.close()

def count_strane(files):
    flag=0
    data=[]
    f=open(files,"r")
    for i in (f):
        if flag == 1:
            data.append(i.split()[1])
        if i.find("[DATA]") == 0:
            flag=1
    f.close()
    return data


def count_tunnal(files,T_start,T_end,S_start,S_end):
    data=readFile_f_tunnel(files)
    line_temp = board_arr(data,T_start,S_end)

    return line_temp

def movement(move):
    newmovment=[]
    counter = 0
    for v in range(-4,5):
        k = []
        b = []
        x = []
        c = 0
        for i in range(4+v,len(move)-4):
            x.append(float(0.5054*c))
            k.append((move[i+1]-move[i])/(0.5054*(c+1)-0.5054*(c)))
            b.append(move[i]-k[c]*x[c])
            c = c + 1


        for f in range(5):
            summ=[]
            counter=counter+1
            newmovment.append([])
            d = open(Tempfile_path+"/"+str(counter)+".txt","w")
            for i in range(len(b)):
                d.write(str(k[i]*(x[i]+f*0.1)+b[i])+"\n")
            d.close()

    return newmovment

def export_base(stend):
    m = open(r"C:\Users\sasha\OneDrive\Рабочий стол\easybrizzy" + "/" + "base" + ".txt", "w")
    for i in range(4,len(stend)):
        m.write(str(stend[i])+"\n")
    m.close()

def find_best(base,path,id,new_file, base_file): # открываем по очереди файлы и ищем минимальную разницу между ними
    file_name=[]
    list=glob.glob(Tempfile_path+"\*.txt")
    all_sum=[]
    for file in list:
        file_name.append(file)
        m = open(file, "r")
        data_move=[]
        for k in m:
            data_move.append((float(k)))
        m.close()
        sumw=0

        for i in range(len(data_move)):

            sumw=sumw+abs(float(base[i])-data_move[i])
        all_sum.append(sumw)

    finde=all_sum.index(min(all_sum))

    try:
        head_text = getgata(new_file, base_file,id)
        name=getname(id)
        read=open(file_name[finde],"r")
        wrt=open(path+"/"+name+'_moved.txt',"w")
        wrt.write(head_text+"\n")
        text=str(min(all_sum))+" "+"\n"
        wrt.write("S= "+text)
        wrt.write("[DATA]"+"\n")
        counter=0
        for i in read:
            counter=counter+1
            if i!="\n":
                wrt.write(str('%.3f' % (0.5054*counter))+" "+str(i))
        wrt.close()
        read.close()
    except Exception as err:
        print(err)
    listtorm = glob.glob(Tempfile_path + "\*")
    for c in listtorm:
        os.remove(c)



list_of_files = glob.glob(Datapath+r"\*") #
for l in list_of_files:  #find all lines
    if l[-2:] == "22":   # find lines
        line="22"
        print(l[-2:])
        for i in glob.glob(l + r"\*\*\*\*"): # serching all folders
            files=glob.glob(i + '/*')
            if len(files) == 1: # if in folder 1 files starting processing
                print(files)
                new_clean_strain = count_tunnal(files[0],c.T_start_2,c.T_end_2,c.S_start_2,c.S_end_2)
                base_clean_strain = count_tunnal(Datapath+"/22/base.txt",c.T_start_2,c.T_end_2,c.S_start_2,c.S_end_2)
                for k in range(4):
                    base_clean_strain.pop(0)
                all_data=movement(new_clean_strain)
                find_best(base_clean_strain,i,line,files[0],Datapath+"/22/base.txt")

                files = glob.glob(i+"\*moved.txt")
                for t in files:

                    new_compare = count_strane(t)
                    print(new_compare)
                    name=getname(line)
                    print("_------------------_")
                    l= open(i+"/"+name+"_basic.txt","w")

                    count=0
                    file_new = glob.glob(i + "\*S.txt")
                    head_text=getgata(file_new[0],Datapath + "/22/base.txt",line)
                    l.write(head_text)
                    l.write("\n"+"[DATA]"+"\n")
                    base=open(i+"/"+"Base.txt",'w')
                    new=open(i+"/"+"New.txt","w")
                    for g in range(len(new_compare)):
                        if 0.5054*g >= 170:
                            count=count+1
                            l.write(str('%.3f' % (0.5054*count))+" "+str((base_clean_strain[g]-float(new_compare[g]))*1000)+'\n')
                            base.write(str(base_clean_strain[g])+"\n")
                            new.write(str(new_compare[g])+"\n")
                    l.close()
                    base.close()
                    new.close()