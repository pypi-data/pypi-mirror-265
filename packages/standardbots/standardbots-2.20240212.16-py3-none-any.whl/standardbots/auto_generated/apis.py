# Code autogenerated by StandardBots
import urllib3
from enum import Enum
import json
from contextlib import contextmanager
from typing import Dict, Generic, TypeVar, Union

from . import models

class RobotKind(Enum):
  Live = "live"
  Simulated = "simulated"

GenericResponseType = TypeVar('GenericResponseType')
OkResponseType = TypeVar('OkResponseType')

class Response(Generic[GenericResponseType, OkResponseType]):
  data: GenericResponseType
  status: int
  response: urllib3.HTTPResponse
  def __init__(self, data: GenericResponseType, status: int, response: urllib3.HTTPResponse):
    self.data = data
    self.status = status
    self.response = response

  def ok(self) -> OkResponseType:
    if self.status != 200:
      raise Exception("Request failed with status " + str(self.status) + ": " + str(self.data))
    return self.data

  def assert_status(self, status: int):
    if self.status != status:
      raise Exception("Expecting status " + str(self.status) + ", but found " + str(self.status))

class RequestManager:
  token: str
  host: str
  robot_kind: RobotKind
  def __init__(
    self,
    http: urllib3.PoolManager,
    token: str,
    host: str,
    robot_kind: RobotKind
  ):
    self.http = http
    self.token = token
    self.host = host
    self.robot_kind = robot_kind

  def request(self, method: str, url: str, **kwargs):
    return self.http.request(method, self.host + url, **kwargs)

  def json_headers(self) -> Dict[str, str]:
    return {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + self.token,
      "robot_kind": self.robot_kind.value,
    }

  def close(self):
    self.http.clear()

class Default:
  _request_manager: RequestManager
  class Equipment:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager

    def onrobot_2fg7_move(
      self,
      value: Union[int, float],
      direction: Union[str, models.LinearGripDirectionEnum] = models.LinearGripDirectionEnum.Inward,
      unit_kind: Union[str, models.LinearUnitKind] = models.LinearUnitKind.Millimeters
    ):
      """Move the robot to the onrobot_2fg7 position.
      """
      return self.control_gripper(
        models.GripperCommandRequest(
          kind=models.GripperKindEnum.Onrobot2Fg7,
          onrobot_2fg7=models.OnRobot2FG7GripperCommandRequest(
            control_kind=models.OnRobot2FG7ControlKindEnum.Move,
            target_grip_width=models.LinearUnit(
              unit_kind=models.LinearUnitKind(unit_kind),
              value=float(value),
            ),
            grip_direction=models.LinearGripDirectionEnum(direction),
          )
        )
      )
    
    def onrobot_2fg7_grip(
      self,
      value: Union[int, float],
      direction: Union[str, models.LinearGripDirectionEnum] = models.LinearGripDirectionEnum.Inward,
      unit_kind: Union[str, models.LinearUnitKind] = models.LinearUnitKind.Millimeters,
      force: Union[int, float] = 0.0,
      force_unit: Union[str, models.ForceUnitKind] = models.ForceUnitKind.Newtons
    ):
      """Move the robot to the onrobot_2fg7 position.
      """
      return self.control_gripper(
        models.GripperCommandRequest(
          kind=models.GripperKindEnum.Onrobot2Fg7,
          onrobot_2fg7=models.OnRobot2FG7GripperCommandRequest(
            control_kind=models.OnRobot2FG7ControlKindEnum.ForceGrip,
            target_grip_width=models.LinearUnit(
              unit_kind=models.LinearUnitKind(unit_kind),
              value=float(value),
            ),
            target_force=models.ForceUnit(
              unit_kind=models.ForceUnitKind(force_unit),
              value=float(force),
            ),
            grip_direction=models.LinearGripDirectionEnum(direction),
          )
        )
      )
    
    def dh_ag_grip(
        self,
        target_diameter: float,
        target_force: float | None,
        target_speed: float | None,
    ):
        """
        Control the DH AG gripper.
        Args:
        - target_diameter: 0.0 - 1.0
        - target_force: 0.2 - 1.0
        - target_speed: 0.01 - 1.0
        """
        return self.control_gripper(
            body=models.GripperCommandRequest(
                kind=models.GripperKindEnum.DhAg,
                dh_ag=models.DHAGGripperCommandRequest(
                    target_diameter, target_force, target_speed
                ),
            ),
        )
    

    def control_gripper(
      self,
      body: models.GripperCommandRequest,
    ) -> Response[
      None,
      None
    ]:
      """
      Send commands to control the Gripper (End Effector) of the robot. The gripper can be any of Standard Bots supported grippers.

      """
      path = "/api/v1/equipment/end-effector/control"
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_gripper_command_request(body)),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def get_gripper_configuration(
      self,
    ) -> Response[
      Union[
        models.GripperConfiguration,
        models.ErrorResponse,
        None
      ],
      models.GripperConfiguration
    ]:
      """
      Get the current gripper configuration

      """
      path = "/api/v1/equipment/end-effector/configuration"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_gripper_configuration(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  class Space:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager


    def list_position(
      self,
      limit: int,
      offset: int,
    ) -> Response[
      Union[
        models.PlanesPaginatedResponse,
        models.ErrorResponse,
        None
      ],
      models.PlanesPaginatedResponse
    ]:
      """
      List Positions
      """
      path = "/api/v1/space/positions"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
        fields={
          "limit": models.serialize_i_64(limit),
          "offset": models.serialize_i_64(offset),
        }
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_planes_paginated_response(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def list_planes(
      self,
      limit: int,
      offset: int,
    ) -> Response[
      Union[
        models.PlanesPaginatedResponse,
        models.ErrorResponse,
        None
      ],
      models.PlanesPaginatedResponse
    ]:
      """
      List Planes
      """
      path = "/api/v1/space/planes"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
        fields={
          "limit": models.serialize_i_64(limit),
          "offset": models.serialize_i_64(offset),
        }
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_planes_paginated_response(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  equipment: Equipment
  space: Space

  def __init__(self, request_manager: RequestManager):
    self._request_manager = request_manager
    self.equipment = Default.Equipment(request_manager)
    self.space = Default.Space(request_manager)

class Movement:
  _request_manager: RequestManager
  class Brakes:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager

    
    def brake(self):
        """Brake the robot
        """
        return self.set_brakes_state(
          models.BrakesState(
            state=models.BrakesStateEnum.Engaged,
          ),
        )
    
    def unbrake(self):
        """Unbrake the robot
        """
        return self.set_brakes_state(
          models.BrakesState(
            state=models.BrakesStateEnum.Disengaged,
          ),
        )
    

    def set_brakes_state(
      self,
      body: models.BrakesState,
    ) -> Response[
      Union[
        models.BrakesState,
        models.ErrorResponse,
        None
      ],
      models.BrakesState
    ]:
      """
      Control Joint Brakes in the robot

      """
      path = "/api/v1/movement/brakes"
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_brakes_state(body)),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_brakes_state(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def get_brakes_state(
      self,
    ) -> Response[
      Union[
        models.BrakesState,
        models.ErrorResponse,
        None
      ],
      models.BrakesState
    ]:
      """
      Get the current state of the robot brakes

      """
      path = "/api/v1/movement/brakes"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_brakes_state(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def engage_emergency_stop(
      self,
      body: models.EngageEmergencyStopRequest,
    ) -> Response[
      None,
      None
    ]:
      """
      Engage Emergency braking system.
&gt; **⚠️ Warning:** This will immediately stop the robot and may cause damage to the robot or surrounding environment.

      """
      path = "/api/v1/movement/brakes/emergency-stop"
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_engage_emergency_stop_request(body)),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  class Position:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager

    def move(
      self,
      position: models.Position,
      orientation: models.Orientation,
      reference_frame: str = 'base',
      axis_alignment: str = 'base'
    ):
      return self.move_tooltip(
        position=position,
        orientation=orientation,
        reference_frame=reference_frame,
        axis_alignment=axis_alignment
      )
    
    def move_tooltip(
      self,
      position: models.Position,
      orientation: models.Orientation,
      reference_frame: str = 'base',
      axis_alignment: str = 'base'
    ):
      """Move tooltip of robot to specified position
      """
      request = models.ArmPositionUpdateRequest(
        kind=models.ArmPositionUpdateRequestKindEnum.TooltipPosition,
        tooltip_position=models.PositionAndOrientation(
          position=position,
          orientation=orientation,
          reference_frame=reference_frame,
          axis_alignment=axis_alignment,
        ),
      )
      return self.set_arm_position(request)
    

    def get_arm_position(
      self,
    ) -> Response[
      Union[
        models.CombinedArmPosition,
        models.ErrorResponse,
        None
      ],
      models.CombinedArmPosition
    ]:
      """
      Get the current position of the robot arm
      """
      path = "/api/v1/movement/position/arm"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_combined_arm_position(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def set_arm_position(
      self,
      body: models.ArmPositionUpdateRequest,
    ) -> Response[
      Union[
        models.ArmPositionUpdateEvent,
        models.ErrorResponse,
        None
      ],
      models.ArmPositionUpdateEvent
    ]:
      """
      Control the position of the RO1 Robot arm.

      """
      path = "/api/v1/movement/position/arm"
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_arm_position_update_request(body)),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_arm_position_update_event(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  brakes: Brakes
  position: Position

  def __init__(self, request_manager: RequestManager):
    self._request_manager = request_manager
    self.brakes = Movement.Brakes(request_manager)
    self.position = Movement.Position(request_manager)

class Camera:
  _request_manager: RequestManager
  class Data:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager


    def get_color_frame(
      self,
      body: models.CameraFrameRequest,
    ) -> Response[
      None,
      None
    ]:
      """
      Retrieve the latest RGB frame from the camera.
      """
      path = "/api/v1/camera/frame/rgb"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_camera_frame_request(body)),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def get_camera_intrinsics_color(
      self,
    ) -> Response[
      None,
      None
    ]:
      """
      Retrieve the intrinsic parameters for the color camera.
      """
      path = "/api/v1/camera/intrinsics/rgb"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def get_camera_stream(
      self,
    ) -> Response[
      None,
      None
    ]:
      """
      Retrieve the latest RGB frame from the camera.
      """
      path = "/api/v1/camera/stream"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  class Settings:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager


    def set_camera_settings(
      self,
      body: models.CameraSettings,
    ) -> Response[
      None,
      None
    ]:
      """
      Set the camera settings.
      """
      path = "/api/v1/camera/settings"
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_camera_settings(body)),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  data: Data
  settings: Settings

  def __init__(self, request_manager: RequestManager):
    self._request_manager = request_manager
    self.data = Camera.Data(request_manager)
    self.settings = Camera.Settings(request_manager)

class RoutineEditor:
  _request_manager: RequestManager
  class Routines:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager


    def play(
      self,
      body: models.PlayRoutineRequest,
      routine_id: str,
    ) -> Response[
      None,
      None
    ]:
      """
      Play a routine
      """
      path = "/api/v1/routine-editor/routines/{routine_id}/play"
      path = path.replace("{routine_id}", str(routine_id))
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_play_routine_request(body)),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def pause(
      self,
      routine_id: str,
    ) -> Response[
      None,
      None
    ]:
      """
      Pause a routine
      """
      path = "/api/v1/routine-editor/routines/{routine_id}/pause"
      path = path.replace("{routine_id}", str(routine_id))
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def stop(
      self,
    ) -> Response[
      None,
      None
    ]:
      """
      Stop running routine and all ongoing motions
      """
      path = "/api/v1/routine-editor/stop"
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def list(
      self,
      limit: int,
      offset: int,
    ) -> Response[
      Union[
        models.RoutinesPaginatedResponse,
        models.ErrorResponse,
        None
      ],
      models.RoutinesPaginatedResponse
    ]:
      """
      List routines defined in Routine Editor UI
      """
      path = "/api/v1/routine-editor/routines"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
        fields={
          "limit": models.serialize_i_64(limit),
          "offset": models.serialize_i_64(offset),
        }
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_routines_paginated_response(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def load(
      self,
      routine_id: str,
    ) -> Response[
      Union[
        models.Routine,
        models.ErrorResponse,
        None
      ],
      models.Routine
    ]:
      """
      Get routine data by ID
      """
      path = "/api/v1/routine-editor/routines/{routine_id}"
      path = path.replace("{routine_id}", str(routine_id))
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_routine(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  class Variables:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager


    def load(
      self,
      variable_id: str,
    ) -> Response[
      Union[
        models.RuntimeVariable,
        models.ErrorResponse,
        None
      ],
      models.RuntimeVariable
    ]:
      """
      Returns current state of a variable
      """
      path = "/api/v1/routine-editor/variables/{variable_id}"
      path = path.replace("{variable_id}", str(variable_id))
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_runtime_variable(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def update(
      self,
      body: models.RuntimeVariable,
      variable_id: str,
    ) -> Response[
      Union[
        models.RuntimeVariable,
        models.ErrorResponse,
        None
      ],
      models.RuntimeVariable
    ]:
      """
      Update the value of a variable
      """
      path = "/api/v1/routine-editor/variables/{variable_id}"
      path = path.replace("{variable_id}", str(variable_id))
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_runtime_variable(body)),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_runtime_variable(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  routines: Routines
  variables: Variables

  def __init__(self, request_manager: RequestManager):
    self._request_manager = request_manager
    self.routines = RoutineEditor.Routines(request_manager)
    self.variables = RoutineEditor.Variables(request_manager)

class Status:
  _request_manager: RequestManager
  class Control:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager


    def set_configuration_control_state(
      self,
      body: models.RobotControlMode,
    ) -> Response[
      Union[
        models.RobotControlMode,
        models.ErrorResponse,
        None
      ],
      models.RobotControlMode
    ]:
      """
      Set the system which is controlling the robot
      """
      path = "/api/v1/status/control-mode"
      response = self._request_manager.request(
        "POST",
        path,
        headers=self._request_manager.json_headers(),
        body=json.dumps(models.serialize_robot_control_mode(body)),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_robot_control_mode(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

    def get_configuration_state_control(
      self,
    ) -> Response[
      Union[
        models.RobotControlMode,
        models.ErrorResponse,
        None
      ],
      models.RobotControlMode
    ]:
      """
      Get the system which is controlling the robot
      """
      path = "/api/v1/status/control-mode"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_robot_control_mode(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  class Health:
    def __init__(self, request_manager: RequestManager):
      self._request_manager = request_manager


    def get_health(
      self,
    ) -> Response[
      Union[
        models.StatusHealthResponse,
        models.ErrorResponse,
        None
      ],
      models.StatusHealthResponse
    ]:
      """
      Get the current health of the robot
      """
      path = "/api/v1/status/health"
      response = self._request_manager.request(
        "GET",
        path,
        headers=self._request_manager.json_headers(),
      )
      parsed = None
      if response.status == 200:
        parsed = models.parse_status_health_response(json.loads(response.data))

      is_user_error = response.status >= 400 and response.status < 500
      is_unavailable = response.status == 503
      if parsed is None and (is_user_error or is_unavailable):
        parsed = models.parse_error_response(json.loads(response.data))

      return Response(
        parsed,
        response.status,
        response
      )

  control: Control
  health: Health

  def __init__(self, request_manager: RequestManager):
    self._request_manager = request_manager
    self.control = Status.Control(request_manager)
    self.health = Status.Health(request_manager)




class StandardBotsRobot(Default):
  RobotKind = RobotKind

  movement: Movement
  camera: Camera
  routine_editor: RoutineEditor
  status: Status
  def __init__(
    self,
    url: str,
    token: str,
    robot_kind: Union[RobotKind, str] = RobotKind.Live,
    pools: int = 10
  ):
    super().__init__(RequestManager(
      urllib3.PoolManager(num_pools=2),
      token=token,
      host=url,
      robot_kind=RobotKind(robot_kind),
    ))
    self.movement = Movement(self._request_manager)
    self.camera = Camera(self._request_manager)
    self.routine_editor = RoutineEditor(self._request_manager)
    self.status = Status(self._request_manager)

  @contextmanager
  def connection(self):
    yield
    self._request_manager.close()

