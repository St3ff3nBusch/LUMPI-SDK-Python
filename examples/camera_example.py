from objects.LUMPIParser import LUMPIParser
from objects.PointCloudFilter import PointCloudFilter
import os
import numpy as np
if __name__ == '__main__':
    lp=LUMPIParser(path="/home/busch/LUMPI_test_data")

    #Initilaize Measurement
    measurement_id=4
    lp.read_point_cloud_file_list(measurement_id)
    print(lp.lidarPath)
    lp.read_all_cameras(measurement_id,True)
    lp.read_track(os.path.join(lp.path,"Measurement"+str(measurement_id),"Label.csv"))
    filter=PointCloudFilter()
    filter.read_background(os.path.join(lp.path,"Measurement"+str(measurement_id),"background"))  
    #Chose camera
    cam=lp.cameras[2]
    time=0
    for i in range(10):
        time+=1./cam.fps
        next_time=time+1/cam.fps
        index=int(np.floor(time*10))
        next_index=int(np.floor(next_time*10))
        if not lp.read_point_cloud(index):
            continue
        cam.set_frame(int(np.floor(time*cam.fps)),True)
        #Filter point cloud by frame time and forground
        fb=filter.filter_background(lp.get_points_meta())
        id2= filter.filter_points_by_time(lp.pc,time,next_time)
        id3=np.intersect1d(fb[0],id2)
        cam.plot_point_cloud(lp.get_xyz()[id3,:],[1,0,0])
        #Read also next point cloud if frame intervall reach also next cloud
        if(next_index-index>0):
            if not lp.read_point_cloud(next_index):
                continue
            #Filter point cloud by frame time and forground
            fb=filter.filter_background(lp.get_points_meta())
            id2= filter.filter_points_by_time(lp.pc,time,next_time)
            id3=np.intersect1d(fb[0],id2)
            cam.plot_point_cloud(lp.get_xyz()[id3,:],[1,0,0])
        #Interpolate bounding boxes to camera frame
        bb=lp.get_bounding_boxes_at(time)
        cam.plot_bounding_boxes_3D(bb,[255,0,0])
        if(27==cam.plot_frame(0)):#exit with ECP
            break
        