from vilib import Vilib

def clamp_number(num,a,b):
    return max(min(num, max(a, b)), min(a, b))

class Camera:
    detectsFace = False
    picarx = None

    x_angle = 0
    y_angle = 0

    def __init__(self, _picarx):
        Vilib.camera_start(vflip=False,hflip=False)
        Vilib.display(local=True,web=True)
        Vilib.face_detect_switch(True)
        self.picarx = _picarx


    def periodic(self):
        self.detectsFace = Vilib.detect_obj_parameter['human_n'] != 0

        if self.detectsFace:
            # change the pan-tilt angle for track the object
            coordinate_x = Vilib.detect_obj_parameter['human_x']
            coordinate_y = Vilib.detect_obj_parameter['human_y']
        
            self.x_angle +=(coordinate_x*10/640)-5
            self.x_angle = clamp_number(self.x_angle,-35,35)
            self.picarx.set_cam_pan_angle(self.x_angle)

            self.y_angle -=(coordinate_y*10/480)-5
            self.y_angle = clamp_number(self.y_angle,-35,35)
            self.picarx.set_cam_tilt_angle(self.y_angle)