from pxr import Usd, UsdGeom, Sdf, Gf

from utils import euler_angles_to_quat, get_bounding_box

# 1. Define stage 
stage = Usd.Stage.CreateNew('six_card_camera.usda')
world_prim = UsdGeom.Xform.Define(stage, '/World')

# 2. Load or create model
UsdGeom.Cube.Define(stage, '/World/model')

###### or you can load your or model from file_path #########
# file_path = "path/to/your/model.usd"
# model_prim = stage.GetPrimAtPath('/World/model')
# if not model_prim.IsValid():
#     robot_prim = stage.DefinePrim('/World/model')
# 
# success_bool = model_prim.GetReferences().AddReference(file_path)

# 3. Get model bounding boxes and calculate camera positions
CAMERA_OFFSET = 100 # a constant distance between camera and the model
bboxes = get_bounding_box(stage, '/World/model')
box_min, box_max = bboxes
box_center = [(box_min[0] + box_max[0]) / 2, (box_min[1] + box_max[1]) / 2, (box_min[2] + box_max[2]) / 2]

front_pos = [box_max[0] + CAMERA_OFFSET, box_center[1], box_center[2]]
front_rot = [0, 90, 0]

back_pos = [box_min[0] - CAMERA_OFFSET, box_center[1], box_center[2]]
back_rot = [0, -90, 0]

left_pos = [box_max[0], box_center[1] - CAMERA_OFFSET, box_center[2]]
left_rot = [90, 0, 0]

right_pos = [box_min[0], box_center[1] + CAMERA_OFFSET, box_center[2]]
right_rot = [-90, 0, 0]

bottom_pos = [box_max[0], box_center[1], box_center[2] - CAMERA_OFFSET]
bottom_rot = [0, 180, 0]

top_pos = [box_min[0], box_center[1], box_center[2] + CAMERA_OFFSET]
top_rot = [0, 0, 0]

camera_names = ["front", "back", "left", "right", "bottom", "top"]
camera_positions = [front_pos, back_pos, left_pos, right_pos, bottom_pos, top_pos]
camera_rotations = [front_rot, back_rot, left_rot, right_rot, bottom_rot, top_rot]

# 3. Add cameras

for i in range(len(camera_positions)):
    camera_pos = camera_positions[i]
    camera_name = camera_names[i]
    camera_rot = camera_rotations[i]

    # UsdGeom.Camera.Define(stage, f"/World/{camera_name}_camera")
    camera_prim = stage.DefinePrim(f"/World/{camera_name}_camera", "Camera")

    camera_translation = Gf.Vec3f(camera_pos) 
    if "xformOp:translate" not in camera_prim.GetPropertyNames():
        UsdGeom.Xformable(camera_prim).AddTranslateOp()
    camera_prim.GetAttribute("xformOp:translate").Set(camera_translation)

    q = euler_angles_to_quat(camera_rot, degrees=True)
    camera_orientation = Gf.Quatf(q[0], q[1], q[2], q[3])
    if "xformOp:orient" not in camera_prim.GetPropertyNames():
        UsdGeom.Xformable(camera_prim).AddOrientOp()
    camera_prim.GetAttribute("xformOp:orient").Set(
        camera_orientation
    )  


stage.GetRootLayer().Save()