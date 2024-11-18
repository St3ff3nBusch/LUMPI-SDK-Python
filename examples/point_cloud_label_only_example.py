from objects.LumpiParser import LumpiParser
from objects.PointCloudFilter import PointCloudFilter
from objects.PointCloudVisualizer import PointCloudVisualizer
import os
import numpy as np
if __name__ == '__main__':
    #Change measurement id
    measurement_id=4
    lp=LumpiParser("/media/busch/ExternSSD1T/Label")
    lp.read_point_cloud_file_list(measurement_id)
    lp.read_track("/media/busch/ExternSSD1T/Label/Measurement4/Label.csv")
    vis=PointCloudVisualizer()
    vis.init_camera(np.array([[100, 100, 5],[-100 ,-100, -5]]),1)
       # Plot bounding boxes
    for  i in lp.indexOrdered:
        vis.vis.clear_geometries()
        for o in lp.indexOrdered[i].values():
            vis.add_bounding_box(o)
        vis.update_view()