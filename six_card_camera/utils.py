import numpy as np
import math

from pxr import Usd, UsdGeom


def euler_angles_to_quat(euler_angles: np.ndarray, degrees: bool = False) -> np.ndarray:
    """Convert Euler XYZ angles to quaternion.

    Args:
        euler_angles (np.ndarray):  Euler XYZ angles.
        degrees (bool, optional): Whether input angles are in degrees. Defaults to False.

    Returns:
        np.ndarray: quaternion (w, x, y, z).
    """
    roll, pitch, yaw = euler_angles
    if degrees:
        roll = math.radians(roll)
        pitch = math.radians(pitch)
        yaw = math.radians(yaw)

    cr = np.cos(roll / 2.0)
    sr = np.sin(roll / 2.0)
    cy = np.cos(yaw / 2.0)
    sy = np.sin(yaw / 2.0)
    cp = np.cos(pitch / 2.0)
    sp = np.sin(pitch / 2.0)
    w = (cr * cp * cy) + (sr * sp * sy)
    x = (sr * cp * cy) - (cr * sp * sy)
    y = (cr * sp * cy) + (sr * cp * sy)
    z = (cr * cp * sy) - (sr * sp * cy)
    return np.array([w, x, y, z])


def get_bounding_box(stage, prim_path: str):
    """
    Get the bounding box of a prim
    """

    purposes = [UsdGeom.Tokens.default_]
    bboxcache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), purposes)
    prim = stage.GetPrimAtPath(prim_path)
    bboxes = bboxcache.ComputeWorldBound(prim)
    # print("bboxes", bboxes)
    game_bboxes = [bboxes.ComputeAlignedRange().GetMin(),bboxes.ComputeAlignedRange().GetMax()]
    
    return game_bboxes