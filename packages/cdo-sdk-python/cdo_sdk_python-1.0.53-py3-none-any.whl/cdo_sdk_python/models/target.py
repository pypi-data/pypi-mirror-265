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

class Target(BaseModel):
    """
    Set of targets that contain the object. A target can be, for example, a device, service, or a shared policy (Ruleset).
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The ID of the target with which the object is associated. A target can be, for example, a device, service, or a shared policy (Ruleset).")
    display_name: Optional[StrictStr] = Field(default=None, description="The display name of the target", alias="displayName")
    type: Optional[StrictStr] = Field(default=None, description="The target type")
    __properties: ClassVar[List[str]] = ["id", "displayName", "type"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['ASA', 'FDM_MANAGED_FTD', 'CDFMC', 'CDFMC_MANAGED_FTD', 'SFCN', 'AWS_VPC', 'ONPREM_FMC', 'MERAKI_MX', 'FDM_RULESET', 'ONPREM_FMC_MANAGED_FTD', 'MCD']):
            raise ValueError("must be one of enum values ('ASA', 'FDM_MANAGED_FTD', 'CDFMC', 'CDFMC_MANAGED_FTD', 'SFCN', 'AWS_VPC', 'ONPREM_FMC', 'MERAKI_MX', 'FDM_RULESET', 'ONPREM_FMC_MANAGED_FTD', 'MCD')")
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
        """Create an instance of Target from a JSON string"""
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
        """Create an instance of Target from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "displayName": obj.get("displayName"),
            "type": obj.get("type")
        })
        return _obj


