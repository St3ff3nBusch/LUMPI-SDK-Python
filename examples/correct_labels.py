from objects.LumpiParser import LumpiParser
import os
import numpy as np
import copy

# Function to correct the visibility of points in tracks
def correct_visibility(lp):
    for(track_id,track) in lp.tracks.items():
        last_visibility=0
        for p in track.values():
            v=p.visibility-last_visibility
            last_visibility=p.visibility
            p.visibility=v

# Function to correct the class of objects in tracks
def correct_class(lp):
    tracks=list(lp.tracks.keys())
    tracks.sort()
    index=0
    camId=0    
    while (index>-1 and index<len(tracks)):
        trackId=tracks[index]
        poseId=-1
        maxVisibility=-1
        for k,p in lp.tracks[trackId].items():
            if(p.visibility > maxVisibility):
                maxVisibility=p.visibility
                tmp = copy.deepcopy(p)
        if(maxVisibility>0):
            boxes={}
            boxes[tmp.id]=(tmp.position,tmp.heading,tmp.dim)   
            for i in range(len(lp.cameras)):
                lp.cameras[i].set_frame(int(np.floor(tmp.time*lp.cameras[i].fps)),True)
                lp.cameras[i].plot_bounding_boxes_3D(boxes, [0,0,255])
                lp.cameras[i].plot_class_label(tmp)
                lp.cameras[i].plot_frame(1)
            key=lp.cameras[-1].plot_frame(0)
            if 27==key:  # Exit with ESC
                break
            elif key == 81:  # Left arrow key
               index-=1
            elif key == 83:  # Right arrow key
                index+=1
            elif key in range(48, 57):  # Number keys 0 to 8
                for p in list(lp.tracks[trackId].values()):
                    p.classId=key-48
        else:  # Invisible object (no points within 3D bounding box)
            index+=1
                     
if __name__ == '__main__':
    lp=LumpiParser(path="/media/busch/home/LUMPI")
    measurement_id=4
    lp.read_all_cameras(measurement_id,True)
    lp.read_track(os.path.join(lp.path,"Measurement"+str(measurement_id),"Label.csv"))
    correct_visibility(lp)
    correct_class(lp)
    lp.write_tracks(os.path.join(lp.path,"Measurement"+str(measurement_id),"Label2.csv"))
