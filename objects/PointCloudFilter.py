import numpy as np
import os
import glob
import csv
class PointCloudFilter:
    def __init__(self):
        self.path={}
        self.background={}
        self.meta={}
        self.meter2distance=1
    def read_background(self, path):
        with open(os.path.join(path,"meta_background.txt"), 'r') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if(row[0]=="azimuth normalizer"):
                    self.meta[row[1]]=float(row[2])
                if(row[0]=="meter to distance"):
                    self.meter2distance=float(row[1])
        files = glob.glob(os.path.join(path,"*.npy"))
        for f in files:
          id=f.split(os.sep)[-1].split(".")[0]
          self.background[id]=np.load(f)
          self.path[id]=np.load(f)
          self.background[id]-=self.meter2distance*0.1# add distance to background 0.1m
    def filter_background(self,pc):
        f=[]
        b=[]
        for i in range(pc.shape[0]):
            if(pc[i,3]<self.background[str(pc[i,0])][int(pc[i,1]) ,int(pc[i,2]*self.meta[str(pc[i,0])])]):
               f.append(i)
            else:
               b.append(i)
        return f,b
    def filter_points_by_time(self, pc, minTime,maxTime):
        minTime=minTime*1000000
        maxTime=maxTime*1000000
        return np.where((pc["time"]<maxTime) & (pc["time"]>minTime))[0]
