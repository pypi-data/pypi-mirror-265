# coding: utf-8

"""
    Cisco Defense Orchestrator API

    Use the interactive documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 0.0.1
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class Icmp6Value(BaseModel):
    """
    Icmp6Value
    """ # noqa: E501
    icmp6_type: Optional[StrictStr] = Field(default=None, alias="icmp6Type")
    icmp6_code: Optional[StrictStr] = Field(default=None, alias="icmp6Code")
    __properties: ClassVar[List[str]] = ["icmp6Type", "icmp6Code"]

    @field_validator('icmp6_type')
    def icmp6_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['ANY', 'DESTINATION_UNREACHABLE', 'PACKET_TOO_BIG', 'TIME_EXCEEDED', 'PARAMETER_PROBLEM', 'ECHO_REQUEST', 'ECHO_REPLY', 'MULTICAST_LISTENER_QUERY', 'MULTICAST_LISTENER_REPORT', 'MULTICAST_LISTENER_DONE', 'ROUTER_SOLICITATION', 'ROUTER_ADVERTISEMENT', 'NEIGHBOUR_SOLICITATION', 'NEIGHBOUR_ADVERTISEMENT', 'REDIRECT_MESSAGE', 'ROUTER_RENUMBERING', 'ICMP_NODE_INFO_QUERY', 'ICMP_NODE_INFO_RESPONSE', 'INVERSE_NEIGHBOR_DISCOVERY_SOLICITATION', 'INVERSE_NEIGHBOR_DISCOVERY_ADVERTISEMENT', 'VER2_MULTICAST_LISTENER_REPORT', 'HOME_AGENT_ADDR_DISCOVERY_REQUEST', 'HOME_AGENT_ADDR_DISCOVERY_REPLY', 'MOBILE_PREFIX_SOLICITATION', 'MOBILE_PREFIX_ADVERTISEMENT', 'CERT_PATH_SOLICITATION', 'CERT_PATH_ADVERTISEMENT', 'ICMP_EXP_MOBILITY_PROTOCOLS', 'MULTICAST_ROUTER_ADVERTISEMENT', 'MULTICAST_ROUTER_SOLICITATION', 'MULTICAST_ROUTER_TERMINATION', 'FMIPV6_MESSAGE', 'RPL_CONTROL_MESSAGE', 'PRIVATE_EXPERIMENTATION', 'PRIVATE_EXPERIMENTATION_EXTENDED']):
            raise ValueError("must be one of enum values ('ANY', 'DESTINATION_UNREACHABLE', 'PACKET_TOO_BIG', 'TIME_EXCEEDED', 'PARAMETER_PROBLEM', 'ECHO_REQUEST', 'ECHO_REPLY', 'MULTICAST_LISTENER_QUERY', 'MULTICAST_LISTENER_REPORT', 'MULTICAST_LISTENER_DONE', 'ROUTER_SOLICITATION', 'ROUTER_ADVERTISEMENT', 'NEIGHBOUR_SOLICITATION', 'NEIGHBOUR_ADVERTISEMENT', 'REDIRECT_MESSAGE', 'ROUTER_RENUMBERING', 'ICMP_NODE_INFO_QUERY', 'ICMP_NODE_INFO_RESPONSE', 'INVERSE_NEIGHBOR_DISCOVERY_SOLICITATION', 'INVERSE_NEIGHBOR_DISCOVERY_ADVERTISEMENT', 'VER2_MULTICAST_LISTENER_REPORT', 'HOME_AGENT_ADDR_DISCOVERY_REQUEST', 'HOME_AGENT_ADDR_DISCOVERY_REPLY', 'MOBILE_PREFIX_SOLICITATION', 'MOBILE_PREFIX_ADVERTISEMENT', 'CERT_PATH_SOLICITATION', 'CERT_PATH_ADVERTISEMENT', 'ICMP_EXP_MOBILITY_PROTOCOLS', 'MULTICAST_ROUTER_ADVERTISEMENT', 'MULTICAST_ROUTER_SOLICITATION', 'MULTICAST_ROUTER_TERMINATION', 'FMIPV6_MESSAGE', 'RPL_CONTROL_MESSAGE', 'PRIVATE_EXPERIMENTATION', 'PRIVATE_EXPERIMENTATION_EXTENDED')")
        return value

    @field_validator('icmp6_code')
    def icmp6_code_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['NO_ROUTE_DEST', 'COMMUNICATION_PROHIBITED', 'BEYOND_SCOPE_SRC_ADDR', 'ADDRESS_UNREACHABLE', 'PORT_UNREACHABLE', 'SOURCE_ADDRESS_FAILED', 'REJECT_ROUTE', 'ERROR_SRC_ROUTING_HEADER', 'HOP_LIMIT_EXCEEDED', 'FRAGMENT_REASSEMBLY_TIME_EXCEEDED', 'ERRONEOUS_HEADER_ENCOUNTERED', 'UNRECOGNIZED_NEXT_HEADER_TYPE_ENCOUNTERED', 'UNRECOGNIZED_IPV6_OPTION_ENCOUNTERED', 'IPV6_FIRST_FRAG_HAS_INCOMPLETE_HEADER_CHAIN', 'SR_UPPER_LAYER_HEADER_ERROR', 'ROUTER_RENUMBERING_COMMAND', 'ROUTER_RENUMBERING_RESULT', 'DATA_CONTAINS_IPV6', 'DATA_CONTAINS_NAME', 'DATA_CONTAINS_IPV4', 'SUCCESSFUL_REPLY', 'RESPONDER_REFUSES_ANSWER', 'QTYPE_UNKNOWN']):
            raise ValueError("must be one of enum values ('NO_ROUTE_DEST', 'COMMUNICATION_PROHIBITED', 'BEYOND_SCOPE_SRC_ADDR', 'ADDRESS_UNREACHABLE', 'PORT_UNREACHABLE', 'SOURCE_ADDRESS_FAILED', 'REJECT_ROUTE', 'ERROR_SRC_ROUTING_HEADER', 'HOP_LIMIT_EXCEEDED', 'FRAGMENT_REASSEMBLY_TIME_EXCEEDED', 'ERRONEOUS_HEADER_ENCOUNTERED', 'UNRECOGNIZED_NEXT_HEADER_TYPE_ENCOUNTERED', 'UNRECOGNIZED_IPV6_OPTION_ENCOUNTERED', 'IPV6_FIRST_FRAG_HAS_INCOMPLETE_HEADER_CHAIN', 'SR_UPPER_LAYER_HEADER_ERROR', 'ROUTER_RENUMBERING_COMMAND', 'ROUTER_RENUMBERING_RESULT', 'DATA_CONTAINS_IPV6', 'DATA_CONTAINS_NAME', 'DATA_CONTAINS_IPV4', 'SUCCESSFUL_REPLY', 'RESPONDER_REFUSES_ANSWER', 'QTYPE_UNKNOWN')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Icmp6Value from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Icmp6Value from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "icmp6Type": obj.get("icmp6Type"),
            "icmp6Code": obj.get("icmp6Code")
        })
        return _obj


