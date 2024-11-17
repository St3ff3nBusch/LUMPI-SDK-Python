from objects.LUMPIParser import LUMPIParser
from objects.PointCloudFilter import PointCloudFilter
from objects.PointCloudVisualizer import PointCloudVisualizer
import os
import numpy as np
if __name__ == '__main__':
    #Change measurement id
    measurement_id=4
    lp=LUMPIParser("/home/busch/LUMPI_test_data")
    lp.read_point_cloud_file_list(measurement_id)
    lp.read_track(os.path.join(lp.path,"Measurement"+str(measurement_id),"Label.csv"))
    filter=PointCloudFilter()
    filter.read_background(os.path.join(lp.path,"Measurement"+str(measurement_id),"background")) 
    lp.read_point_cloud(0)
    vis=PointCloudVisualizer()
    vis.init_camera(lp.get_xyz(),10)
    for i in range(len(lp.point_cloud_files)):
        vis.vis.clear_geometries()
        lp.read_point_cloud(i)
        #Filter background
        f,b= filter.filter_background(lp.get_points_meta())
        #Coloring background and foreground
        colors=np.zeros((lp.get_xyz().shape[0],3))
        colors[f]=[0,0,0]
        colors[b]=[0.7,0.7,0.7]   
        vis.add_colored_cloud(lp.get_xyz(),colors)
        #Plot bounding boxes
        if i in lp.indexOrdered:
            for o in lp.indexOrdered[i].values():
                vis.add_bounding_box(o)
        vis.update_view()
  