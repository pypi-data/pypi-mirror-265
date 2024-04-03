from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_router_function_expression import WorkflowRouterFunctionExpression
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowRouterFunction")


@attr.s(auto_attribs=True, repr=False)
class WorkflowRouterFunction:
    """  """

    _edge_config_id: Union[Unset, str] = UNSET
    _expression: Union[Unset, WorkflowRouterFunctionExpression] = UNSET
    _id: Union[Unset, str] = UNSET
    _is_default: Union[Unset, None] = UNSET
    _name: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("edge_config_id={}".format(repr(self._edge_config_id)))
        fields.append("expression={}".format(repr(self._expression)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("is_default={}".format(repr(self._is_default)))
        fields.append("name={}".format(repr(self._name)))
        return "WorkflowRouterFunction({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        edge_config_id = self._edge_config_id
        expression: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._expression, Unset):
            expression = self._expression.to_dict()

        id = self._id
        is_default = None

        name = self._name

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if edge_config_id is not UNSET:
            field_dict["edgeConfigId"] = edge_config_id
        if expression is not UNSET:
            field_dict["expression"] = expression
        if id is not UNSET:
            field_dict["id"] = id
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_edge_config_id() -> Union[Unset, str]:
            edge_config_id = d.pop("edgeConfigId")
            return edge_config_id

        try:
            edge_config_id = get_edge_config_id()
        except KeyError:
            if strict:
                raise
            edge_config_id = cast(Union[Unset, str], UNSET)

        def get_expression() -> Union[Unset, WorkflowRouterFunctionExpression]:
            expression: Union[Unset, Union[Unset, WorkflowRouterFunctionExpression]] = UNSET
            _expression = d.pop("expression")

            if not isinstance(_expression, Unset):
                expression = WorkflowRouterFunctionExpression.from_dict(_expression)

            return expression

        try:
            expression = get_expression()
        except KeyError:
            if strict:
                raise
            expression = cast(Union[Unset, WorkflowRouterFunctionExpression], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_is_default() -> Union[Unset, None]:
            is_default = None

            return is_default

        try:
            is_default = get_is_default()
        except KeyError:
            if strict:
                raise
            is_default = cast(Union[Unset, None], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        workflow_router_function = cls(
            edge_config_id=edge_config_id,
            expression=expression,
            id=id,
            is_default=is_default,
            name=name,
        )

        return workflow_router_function

    @property
    def edge_config_id(self) -> str:
        """ The ID of the workflow flowchart edge config associated with this function """
        if isinstance(self._edge_config_id, Unset):
            raise NotPresentError(self, "edge_config_id")
        return self._edge_config_id

    @edge_config_id.setter
    def edge_config_id(self, value: str) -> None:
        self._edge_config_id = value

    @edge_config_id.deleter
    def edge_config_id(self) -> None:
        self._edge_config_id = UNSET

    @property
    def expression(self) -> WorkflowRouterFunctionExpression:
        """ A JSON object representing the expression associated with this function """
        if isinstance(self._expression, Unset):
            raise NotPresentError(self, "expression")
        return self._expression

    @expression.setter
    def expression(self, value: WorkflowRouterFunctionExpression) -> None:
        self._expression = value

    @expression.deleter
    def expression(self) -> None:
        self._expression = UNSET

    @property
    def id(self) -> str:
        """ The function associated with a router node """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def is_default(self) -> None:
        if isinstance(self._is_default, Unset):
            raise NotPresentError(self, "is_default")
        return self._is_default

    @is_default.setter
    def is_default(self, value: None) -> None:
        self._is_default = value

    @is_default.deleter
    def is_default(self) -> None:
        self._is_default = UNSET

    @property
    def name(self) -> str:
        """ The name of a function associated with a router node """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
