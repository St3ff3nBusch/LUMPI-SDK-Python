from objects.LumpiParser import LumpiParser
import os
if __name__ == '__main__':
    lp=LumpiParser(path="/media/busch/ExternSSD1T/Label")
    measurement_id=3
    lp.read_track(os.path.join(lp.path,"Measurement"+str(measurement_id),"Label.csv"))
    lp.read_all_cameras(measurement_id,True)
    cam=lp.cameras[1]#chose camera
    for i in range(1000):
        cam.set_frame(i,True)
        bb=lp.get_bounding_boxes_at(i/cam.fps)
        cam.plot_bounding_boxes_3D(bb,[0,255,0])
        k=cam.plot_frame(0)
        if(27==k):#Exit with ECP key
            break
        