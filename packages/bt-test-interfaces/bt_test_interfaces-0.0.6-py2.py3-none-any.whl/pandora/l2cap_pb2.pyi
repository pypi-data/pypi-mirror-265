# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generated python gRPC interfaces."""

from __future__ import annotations



from google.protobuf import any_pb2
from google.protobuf import empty_pb2
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper
from google.protobuf.message import Message
from pandora import host_pb2
from typing import Optional
from typing import Union
from typing_extensions import Literal
from typing_extensions import TypedDict

class CommandRejectReason(int, EnumTypeWrapper):
  pass

COMMAND_NOT_UNDERSTOOD: CommandRejectReason
SIGNAL_MTU_EXCEEDED: CommandRejectReason
INVALID_CID_IN_REQUEST: CommandRejectReason


class Channel(Message):
  cookie: any_pb2.Any

  def __init__(self, cookie: any_pb2.Any = any_pb2.Any()) -> None: ...

class FixedChannel(Message):
  connection: host_pb2.Connection
  cid: int

  def __init__(self, connection: host_pb2.Connection = host_pb2.Connection(), cid: int = 0) -> None: ...

class ConnectionOrientedChannelRequest(Message):
  psm: int
  mtu: int

  def __init__(self, psm: int = 0, mtu: int = 0) -> None: ...

class CreditBasedChannelRequest(Message):
  spsm: int
  mtu: int
  mps: int
  initial_credit: int

  def __init__(self, spsm: int = 0, mtu: int = 0, mps: int = 0, initial_credit: int = 0) -> None: ...

class ConnectRequest(Message):
  connection: host_pb2.Connection
  basic: Optional[ConnectionOrientedChannelRequest]
  le_credit_based: Optional[CreditBasedChannelRequest]
  enhanced_credit_based: Optional[CreditBasedChannelRequest]

  def __init__(self, connection: host_pb2.Connection = host_pb2.Connection(), basic: Optional[ConnectionOrientedChannelRequest] = None, le_credit_based: Optional[CreditBasedChannelRequest] = None, enhanced_credit_based: Optional[CreditBasedChannelRequest] = None) -> None: ...

  @property
  def type(self) -> Union[ConnectionOrientedChannelRequest, CreditBasedChannelRequest, None]: ...
  def type_variant(self) -> Union[Literal['basic'], Literal['le_credit_based'], Literal['enhanced_credit_based'], None]: ...
  def type_asdict(self) -> ConnectRequest_type_dict: ...

class ConnectRequest_type_dict(TypedDict, total=False):
  basic: ConnectionOrientedChannelRequest
  le_credit_based: CreditBasedChannelRequest
  enhanced_credit_based: CreditBasedChannelRequest

class ConnectResponse(Message):
  error: Optional[CommandRejectReason]
  channel: Optional[Channel]

  def __init__(self, error: Optional[CommandRejectReason] = None, channel: Optional[Channel] = None) -> None: ...

  @property
  def result(self) -> Union[Channel, CommandRejectReason, None]: ...
  def result_variant(self) -> Union[Literal['error'], Literal['channel'], None]: ...
  def result_asdict(self) -> ConnectResponse_result_dict: ...

class ConnectResponse_result_dict(TypedDict, total=False):
  error: CommandRejectReason
  channel: Channel

class WaitConnectionRequest(Message):
  connection: host_pb2.Connection
  basic: Optional[ConnectionOrientedChannelRequest]
  le_credit_based: Optional[CreditBasedChannelRequest]
  enhanced_credit_based: Optional[CreditBasedChannelRequest]

  def __init__(self, connection: host_pb2.Connection = host_pb2.Connection(), basic: Optional[ConnectionOrientedChannelRequest] = None, le_credit_based: Optional[CreditBasedChannelRequest] = None, enhanced_credit_based: Optional[CreditBasedChannelRequest] = None) -> None: ...

  @property
  def type(self) -> Union[ConnectionOrientedChannelRequest, CreditBasedChannelRequest, None]: ...
  def type_variant(self) -> Union[Literal['basic'], Literal['le_credit_based'], Literal['enhanced_credit_based'], None]: ...
  def type_asdict(self) -> WaitConnectionRequest_type_dict: ...

class WaitConnectionRequest_type_dict(TypedDict, total=False):
  basic: ConnectionOrientedChannelRequest
  le_credit_based: CreditBasedChannelRequest
  enhanced_credit_based: CreditBasedChannelRequest

class WaitConnectionResponse(Message):
  error: Optional[CommandRejectReason]
  channel: Optional[Channel]

  def __init__(self, error: Optional[CommandRejectReason] = None, channel: Optional[Channel] = None) -> None: ...

  @property
  def result(self) -> Union[Channel, CommandRejectReason, None]: ...
  def result_variant(self) -> Union[Literal['error'], Literal['channel'], None]: ...
  def result_asdict(self) -> WaitConnectionResponse_result_dict: ...

class WaitConnectionResponse_result_dict(TypedDict, total=False):
  error: CommandRejectReason
  channel: Channel

class DisconnectRequest(Message):
  channel: Channel

  def __init__(self, channel: Channel = Channel()) -> None: ...

class DisconnectResponse(Message):
  error: Optional[CommandRejectReason]
  success: Optional[empty_pb2.Empty]

  def __init__(self, error: Optional[CommandRejectReason] = None, success: Optional[empty_pb2.Empty] = None) -> None: ...

  @property
  def result(self) -> Union[CommandRejectReason, None, empty_pb2.Empty]: ...
  def result_variant(self) -> Union[Literal['error'], Literal['success'], None]: ...
  def result_asdict(self) -> DisconnectResponse_result_dict: ...

class DisconnectResponse_result_dict(TypedDict, total=False):
  error: CommandRejectReason
  success: empty_pb2.Empty

class WaitDisconnectionRequest(Message):
  channel: Channel

  def __init__(self, channel: Channel = Channel()) -> None: ...

class WaitDisconnectionResponse(Message):
  error: Optional[CommandRejectReason]
  success: Optional[empty_pb2.Empty]

  def __init__(self, error: Optional[CommandRejectReason] = None, success: Optional[empty_pb2.Empty] = None) -> None: ...

  @property
  def result(self) -> Union[CommandRejectReason, None, empty_pb2.Empty]: ...
  def result_variant(self) -> Union[Literal['error'], Literal['success'], None]: ...
  def result_asdict(self) -> WaitDisconnectionResponse_result_dict: ...

class WaitDisconnectionResponse_result_dict(TypedDict, total=False):
  error: CommandRejectReason
  success: empty_pb2.Empty

class ReceiveRequest(Message):
  channel: Optional[Channel]
  fixed_channel: Optional[FixedChannel]

  def __init__(self, channel: Optional[Channel] = None, fixed_channel: Optional[FixedChannel] = None) -> None: ...

  @property
  def source(self) -> Union[Channel, FixedChannel, None]: ...
  def source_variant(self) -> Union[Literal['channel'], Literal['fixed_channel'], None]: ...
  def source_asdict(self) -> ReceiveRequest_source_dict: ...

class ReceiveRequest_source_dict(TypedDict, total=False):
  channel: Channel
  fixed_channel: FixedChannel

class ReceiveResponse(Message):
  data: bytes

  def __init__(self, data: bytes = b'') -> None: ...

class SendRequest(Message):
  data: bytes
  channel: Optional[Channel]
  fixed_channel: Optional[FixedChannel]

  def __init__(self, data: bytes = b'', channel: Optional[Channel] = None, fixed_channel: Optional[FixedChannel] = None) -> None: ...

  @property
  def sink(self) -> Union[Channel, FixedChannel, None]: ...
  def sink_variant(self) -> Union[Literal['channel'], Literal['fixed_channel'], None]: ...
  def sink_asdict(self) -> SendRequest_sink_dict: ...

class SendRequest_sink_dict(TypedDict, total=False):
  channel: Channel
  fixed_channel: FixedChannel

class SendResponse(Message):
  error: Optional[CommandRejectReason]
  success: Optional[empty_pb2.Empty]

  def __init__(self, error: Optional[CommandRejectReason] = None, success: Optional[empty_pb2.Empty] = None) -> None: ...

  @property
  def result(self) -> Union[CommandRejectReason, None, empty_pb2.Empty]: ...
  def result_variant(self) -> Union[Literal['error'], Literal['success'], None]: ...
  def result_asdict(self) -> SendResponse_result_dict: ...

class SendResponse_result_dict(TypedDict, total=False):
  error: CommandRejectReason
  success: empty_pb2.Empty

