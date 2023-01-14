# The Notices and Disclaimers for Ocean Worlds Autonomy Testbed for Exploration
# Research and Simulation can be found in README.md in the root directory of
# this repository.

"""Defines functions required by multiple modules within the package"""

from math import pi, tau, acos, sqrt
from ow_lander import constants
from std_msgs.msg import Header
from rospy import Time
# import roslib; roslib.load_manifest('urdfdom_py')
from urdf_parser_py.urdf import URDF

class Singleton(type):
  """When passed to the metaclass parameter in the class definition, the class
  will behave like a singleton.
  """
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]

def is_shou_yaw_goal_in_range(joint_goal):
  """
  # type joint_goal: List[float, float, float, float, float, float]
  """
  # If shoulder yaw goal angle is out of joint range, abort
  upper = URDF.from_parameter_server().joint_map["j_shou_yaw"].limit.upper
  lower = URDF.from_parameter_server().joint_map["j_shou_yaw"].limit.lower

  if (joint_goal[constants.J_SHOU_YAW]<lower) or (joint_goal[constants.J_SHOU_YAW]>upper):
    return False
  else:
    return True

def _normalize_radians(angle):
  """
  :param angle: (float)
  :return: (float) the angle in [-pi, pi)
  """
  # Note: tau = 2 * pi
  return (angle + pi) % tau - pi

def radians_equivalent(angle1, angle2, tolerance) :
  return abs(_normalize_radians(angle1 - angle2)) <= tolerance

def in_closed_range(val, lo, hi, tolerance):
  """
  :param val, lo, hi, tolerance: (any mutually comparable types)
  :return: (bool)
  """
  return val >= lo-tolerance and val <= hi+tolerance

def poses_approx_equivalent(pose1, pose2, \
    meter_tolerance=constants.ARM_POSE_METER_TOLERANCE, \
    radian_tolerance=constants.ARM_POSE_RADIAN_TOLERANCE):
  p1 = pose1.position
  p2 = pose2.position
  distance = sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
  if distance <= meter_tolerance:
    o1 = pose1.orientation
    o2 = pose2.orientation
    # check that the geodesic norm between the 2 quaternions is below tolerance
    dp = o1.x * o2.x + o1.y * o2.y + o1.z * o2.z + o1.w * o2.w
    if acos(2*dp*dp-1) <= radian_tolerance:
      return True
  return False

def create_most_recent_header(frame_id):
  return Header(0, Time(0), frame_id)
