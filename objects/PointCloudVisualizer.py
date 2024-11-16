import open3d as o3d
class PointCloudVisualizer:
    def __init__(self):
        self.vis=o3d.visualization.VisualizerWithKeyCallback()#o3d.visualization.Visualizer()
        self.lines= [[0, 1], [1, 2], [2, 3], [0, 3],
        [4, 5], [5, 6], [6, 7], [4, 7],
        [0, 4], [1, 5], [2, 6], [3, 7]]
        self.colors = [[0, 0, 1] for _ in range(len(self.lines))]
    def init_camera(self, pts, time):
        self.vis.create_window()
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pts)
        self.vis.add_geometry(pcd)
        for i in range(time):
            self.vis.poll_events()
            self.vis.update_renderer()
            self.vis.get_render_option().point_size = 3    
            from time import sleep
            sleep(0.05)
        self.camera=self.vis.get_view_control().convert_to_pinhole_camera_parameters()
    def update_view(self):
        self.vis.get_view_control().convert_from_pinhole_camera_parameters(self.camera,True)
        self.vis.poll_events()
        self.vis.update_renderer()
        self.camera=self.vis.get_view_control().convert_to_pinhole_camera_parameters()
    def add_bounding_box(self,p):
        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector(p.corners.transpose())
        line_set.lines = o3d.utility.Vector2iVector(self.lines)
        line_set.colors = o3d.utility.Vector3dVector(self.colors)
        self.vis.add_geometry(line_set)
    def add_colored_cloud(self,pts,colors):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pts)
        pcd.colors = o3d.utility.Vector3dVector(colors)     
        self.vis.add_geometry(pcd)