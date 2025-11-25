"""
Tests para las enumeraciones de dominio (US-1.1).

Verifica que:
- Todos los enums tienen los valores esperados
- Los enums son serializables a string
- Los enums son importables desde society_sim.domain
"""

import json

import pytest

from society_sim.domain import EventType, IdeologicalBias, Sector
from society_sim.domain.enums import EventType as DirectEventType
from society_sim.domain.enums import IdeologicalBias as DirectIdeologicalBias
from society_sim.domain.enums import Sector as DirectSector


class TestSectorEnum:
    """Tests para el enum Sector."""

    def test_sector_has_all_expected_values(self) -> None:
        """Verifica que Sector tiene todos los valores definidos en US-1.1."""
        expected_values = {"HOUSING", "FOOD", "TECHNOLOGY", "CONSTRUCTION", "HEALTHCARE", "FINANCE"}
        actual_values = {member.name for member in Sector}

        assert actual_values == expected_values

    def test_sector_count(self) -> None:
        """Verifica que hay exactamente 6 sectores."""
        assert len(Sector) == 6

    def test_sector_values_are_lowercase_strings(self) -> None:
        """Verifica que los valores del enum son strings en minúsculas."""
        for sector in Sector:
            assert isinstance(sector.value, str)
            assert sector.value == sector.value.lower()

    @pytest.mark.parametrize(
        "sector,expected_value",
        [
            (Sector.HOUSING, "housing"),
            (Sector.FOOD, "food"),
            (Sector.TECHNOLOGY, "technology"),
            (Sector.CONSTRUCTION, "construction"),
            (Sector.HEALTHCARE, "healthcare"),
            (Sector.FINANCE, "finance"),
        ],
    )
    def test_sector_individual_values(self, sector: Sector, expected_value: str) -> None:
        """Verifica que cada sector tiene el valor esperado."""
        assert sector.value == expected_value

    def test_sector_serializable_to_string(self) -> None:
        """Verifica que Sector es serializable a string (requisito US-1.1.4)."""
        for sector in Sector:
            # Debe ser convertible a string
            str_value = str(sector)
            assert isinstance(str_value, str)
            assert len(str_value) > 0

            # El valor del StrEnum debe ser el string
            assert sector.value == str_value

    def test_sector_json_serializable(self) -> None:
        """Verifica que Sector es serializable a JSON."""
        for sector in Sector:
            # Debe poder serializarse a JSON sin errores
            json_str = json.dumps({"sector": sector.value})
            assert isinstance(json_str, str)

            # Debe poder deserializarse
            data = json.loads(json_str)
            assert data["sector"] == sector.value


class TestEventTypeEnum:
    """Tests para el enum EventType."""

    def test_event_type_has_all_expected_values(self) -> None:
        """Verifica que EventType tiene todos los valores definidos en US-1.1."""
        expected_values = {
            "COMPANY_SCANDAL",
            "COMPANY_SUCCESS",
            "SECTOR_CRISIS",
            "SECTOR_BOOM",
            "PARTY_SCANDAL",
            "PARTY_SUCCESS",
            "POLICY_PROPOSAL",
        }
        actual_values = {member.name for member in EventType}

        assert actual_values == expected_values

    def test_event_type_count(self) -> None:
        """Verifica que hay exactamente 7 tipos de evento."""
        assert len(EventType) == 7

    def test_event_type_values_are_lowercase_strings(self) -> None:
        """Verifica que los valores del enum son strings en minúsculas."""
        for event_type in EventType:
            assert isinstance(event_type.value, str)
            assert event_type.value == event_type.value.lower()

    @pytest.mark.parametrize(
        "event_type,expected_value",
        [
            (EventType.COMPANY_SCANDAL, "company_scandal"),
            (EventType.COMPANY_SUCCESS, "company_success"),
            (EventType.SECTOR_CRISIS, "sector_crisis"),
            (EventType.SECTOR_BOOM, "sector_boom"),
            (EventType.PARTY_SCANDAL, "party_scandal"),
            (EventType.PARTY_SUCCESS, "party_success"),
            (EventType.POLICY_PROPOSAL, "policy_proposal"),
        ],
    )
    def test_event_type_individual_values(self, event_type: EventType, expected_value: str) -> None:
        """Verifica que cada tipo de evento tiene el valor esperado."""
        assert event_type.value == expected_value

    def test_event_type_serializable_to_string(self) -> None:
        """Verifica que EventType es serializable a string (requisito US-1.1.4)."""
        for event_type in EventType:
            str_value = str(event_type)
            assert isinstance(str_value, str)
            assert len(str_value) > 0
            assert event_type.value == str_value

    def test_event_type_json_serializable(self) -> None:
        """Verifica que EventType es serializable a JSON."""
        for event_type in EventType:
            json_str = json.dumps({"event_type": event_type.value})
            assert isinstance(json_str, str)

            data = json.loads(json_str)
            assert data["event_type"] == event_type.value

    def test_event_types_categorization(self) -> None:
        """Verifica que los tipos de evento se pueden categorizar correctamente."""
        company_events = [EventType.COMPANY_SCANDAL, EventType.COMPANY_SUCCESS]
        sector_events = [EventType.SECTOR_CRISIS, EventType.SECTOR_BOOM]
        party_events = [EventType.PARTY_SCANDAL, EventType.PARTY_SUCCESS]
        policy_events = [EventType.POLICY_PROPOSAL]

        all_events = company_events + sector_events + party_events + policy_events
        assert len(all_events) == len(EventType)

        for event in company_events:
            assert "company" in event.value

        for event in sector_events:
            assert "sector" in event.value

        for event in party_events:
            assert "party" in event.value


class TestIdeologicalBiasEnum:
    """Tests para el enum IdeologicalBias."""

    def test_ideological_bias_has_all_expected_values(self) -> None:
        """Verifica que IdeologicalBias tiene todos los valores definidos en US-1.1."""
        expected_values = {"LEFT", "CENTER_LEFT", "CENTER", "CENTER_RIGHT", "RIGHT"}
        actual_values = {member.name for member in IdeologicalBias}

        assert actual_values == expected_values

    def test_ideological_bias_count(self) -> None:
        """Verifica que hay exactamente 5 orientaciones ideológicas."""
        assert len(IdeologicalBias) == 5

    def test_ideological_bias_values_are_lowercase_strings(self) -> None:
        """Verifica que los valores del enum son strings en minúsculas."""
        for bias in IdeologicalBias:
            assert isinstance(bias.value, str)
            assert bias.value == bias.value.lower()

    @pytest.mark.parametrize(
        "bias,expected_value",
        [
            (IdeologicalBias.LEFT, "left"),
            (IdeologicalBias.CENTER_LEFT, "center_left"),
            (IdeologicalBias.CENTER, "center"),
            (IdeologicalBias.CENTER_RIGHT, "center_right"),
            (IdeologicalBias.RIGHT, "right"),
        ],
    )
    def test_ideological_bias_individual_values(
        self, bias: IdeologicalBias, expected_value: str
    ) -> None:
        """Verifica que cada orientación ideológica tiene el valor esperado."""
        assert bias.value == expected_value

    def test_ideological_bias_serializable_to_string(self) -> None:
        """Verifica que IdeologicalBias es serializable a string (requisito US-1.1.4)."""
        for bias in IdeologicalBias:
            str_value = str(bias)
            assert isinstance(str_value, str)
            assert len(str_value) > 0
            assert bias.value == str_value

    def test_ideological_bias_json_serializable(self) -> None:
        """Verifica que IdeologicalBias es serializable a JSON."""
        for bias in IdeologicalBias:
            json_str = json.dumps({"ideology": bias.value})
            assert isinstance(json_str, str)

            data = json.loads(json_str)
            assert data["ideology"] == bias.value

    def test_ideological_spectrum_order(self) -> None:
        """Verifica que el espectro ideológico tiene un orden lógico."""
        spectrum = [
            IdeologicalBias.LEFT,
            IdeologicalBias.CENTER_LEFT,
            IdeologicalBias.CENTER,
            IdeologicalBias.CENTER_RIGHT,
            IdeologicalBias.RIGHT,
        ]
        # Verificar que todos los valores están representados
        assert set(spectrum) == set(IdeologicalBias)


class TestEnumsImportability:
    """Tests para verificar que los enums son importables desde society_sim.domain."""

    def test_sector_importable_from_domain(self) -> None:
        """Verifica que Sector es importable desde society_sim.domain."""
        assert Sector is DirectSector

    def test_event_type_importable_from_domain(self) -> None:
        """Verifica que EventType es importable desde society_sim.domain."""
        assert EventType is DirectEventType

    def test_ideological_bias_importable_from_domain(self) -> None:
        """Verifica que IdeologicalBias es importable desde society_sim.domain."""
        assert IdeologicalBias is DirectIdeologicalBias

    def test_all_enums_in_domain_all(self) -> None:
        """Verifica que todos los enums están en __all__ del módulo domain."""
        from society_sim import domain

        assert "Sector" in domain.__all__
        assert "EventType" in domain.__all__
        assert "IdeologicalBias" in domain.__all__


class TestEnumsStrEnumBehavior:
    """Tests para verificar el comportamiento de StrEnum."""

    def test_sector_is_str_subclass(self) -> None:
        """Verifica que Sector hereda de str."""
        for sector in Sector:
            assert isinstance(sector, str)

    def test_event_type_is_str_subclass(self) -> None:
        """Verifica que EventType hereda de str."""
        for event_type in EventType:
            assert isinstance(event_type, str)

    def test_ideological_bias_is_str_subclass(self) -> None:
        """Verifica que IdeologicalBias hereda de str."""
        for bias in IdeologicalBias:
            assert isinstance(bias, str)

    def test_enums_can_be_used_as_dict_keys(self) -> None:
        """Verifica que los enums pueden usarse como claves de diccionario."""
        sector_dict = {Sector.HOUSING: 100, Sector.FOOD: 200}
        assert sector_dict[Sector.HOUSING] == 100

        event_dict = {EventType.COMPANY_SCANDAL: "bad", EventType.COMPANY_SUCCESS: "good"}
        assert event_dict[EventType.COMPANY_SCANDAL] == "bad"

        bias_dict = {IdeologicalBias.LEFT: -1, IdeologicalBias.RIGHT: 1}
        assert bias_dict[IdeologicalBias.LEFT] == -1

    def test_enums_equality_with_strings(self) -> None:
        """Verifica que los enums pueden compararse con strings (comportamiento StrEnum)."""
        assert Sector.HOUSING == "housing"
        assert EventType.COMPANY_SCANDAL == "company_scandal"
        assert IdeologicalBias.CENTER == "center"

    def test_enums_can_be_concatenated(self) -> None:
        """Verifica que los enums pueden concatenarse como strings."""
        result = "Sector: " + Sector.HOUSING
        assert result == "Sector: housing"

        result = f"Event: {EventType.PARTY_SCANDAL}"
        assert result == "Event: party_scandal"

