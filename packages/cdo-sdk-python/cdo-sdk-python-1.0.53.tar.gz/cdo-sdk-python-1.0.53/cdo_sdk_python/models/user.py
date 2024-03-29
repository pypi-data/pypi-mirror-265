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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from cdo_sdk_python.models.user_role import UserRole
from typing import Optional, Set
from typing_extensions import Self

class User(BaseModel):
    """
    User
    """ # noqa: E501
    uid: Optional[StrictStr] = Field(default=None, description="The unique identifier of the SDC in CDO.")
    name: Optional[StrictStr] = Field(default=None, description="The name of the user in CDO.")
    roles: Optional[List[UserRole]] = Field(default=None, description="Roles associated with this user in CDO.")
    api_only_user: Optional[StrictBool] = Field(default=None, description="Whether the user is API-only, an API-only user cannot access CDO in the UI.", alias="apiOnlyUser")
    last_successful_login: Optional[datetime] = Field(default=None, description="The time (UTC; represented using the RFC-3339 standard) that indicate the last time the user successfully login CDO.", alias="lastSuccessfulLogin")
    __properties: ClassVar[List[str]] = ["uid", "name", "roles", "apiOnlyUser", "lastSuccessfulLogin"]

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
        """Create an instance of User from a JSON string"""
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
        """Create an instance of User from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "uid": obj.get("uid"),
            "name": obj.get("name"),
            "roles": obj.get("roles"),
            "apiOnlyUser": obj.get("apiOnlyUser"),
            "lastSuccessfulLogin": obj.get("lastSuccessfulLogin")
        })
        return _obj


