from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.generation_tone import GenerationTone
from ..models.scenario_type import ScenarioType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScenarioSetGenerate")


@_attrs_define
class ScenarioSetGenerate:
    """
    Attributes:
        source_scenario_id (str): ID for the scenario set that the generated scenario set will use as a source
        name (str): Name of the generated scenario set
        number_examples (int): Number of examples to be generated for the scenario set
        project_id (Union[Unset, str]): ID for the project
        generation_type (Union[Unset, ScenarioType]): An enumeration. Default: ScenarioType.REPHRASE_INVARIANT.
        generation_tone (Union[Unset, GenerationTone]): An enumeration. Default: GenerationTone.NEUTRAL.
    """

    source_scenario_id: str
    name: str
    number_examples: int
    project_id: Union[Unset, str] = UNSET
    generation_type: Union[Unset, ScenarioType] = ScenarioType.REPHRASE_INVARIANT
    generation_tone: Union[Unset, GenerationTone] = GenerationTone.NEUTRAL
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source_scenario_id = self.source_scenario_id
        name = self.name
        number_examples = self.number_examples
        project_id = self.project_id
        generation_type: Union[Unset, str] = UNSET
        if not isinstance(self.generation_type, Unset):
            generation_type = self.generation_type.value

        generation_tone: Union[Unset, str] = UNSET
        if not isinstance(self.generation_tone, Unset):
            generation_tone = self.generation_tone.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_scenario_id": source_scenario_id,
                "name": name,
                "number_examples": number_examples,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if generation_type is not UNSET:
            field_dict["generation_type"] = generation_type
        if generation_tone is not UNSET:
            field_dict["generation_tone"] = generation_tone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source_scenario_id = d.pop("source_scenario_id")

        name = d.pop("name")

        number_examples = d.pop("number_examples")

        project_id = d.pop("project_id", UNSET)

        _generation_type = d.pop("generation_type", UNSET)
        generation_type: Union[Unset, ScenarioType]
        if isinstance(_generation_type, Unset):
            generation_type = UNSET
        else:
            generation_type = ScenarioType(_generation_type)

        _generation_tone = d.pop("generation_tone", UNSET)
        generation_tone: Union[Unset, GenerationTone]
        if isinstance(_generation_tone, Unset):
            generation_tone = UNSET
        else:
            generation_tone = GenerationTone(_generation_tone)

        scenario_set_generate = cls(
            source_scenario_id=source_scenario_id,
            name=name,
            number_examples=number_examples,
            project_id=project_id,
            generation_type=generation_type,
            generation_tone=generation_tone,
        )

        scenario_set_generate.additional_properties = d
        return scenario_set_generate

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
