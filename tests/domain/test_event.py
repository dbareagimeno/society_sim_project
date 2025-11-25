"""
Tests unitarios para el modelo Event y EventEffect.

Verifica la creación, validación y serialización de eventos
en la simulación.
"""

import json

import pytest
from pydantic import ValidationError

from society_sim.domain import Event, EventEffect, EventType, Sector


class TestEventEffect:
    """Tests para la clase EventEffect."""

    def test_create_event_effect_with_defaults(self):
        """EventEffect se puede crear con todos los valores por defecto."""
        effect = EventEffect()

        assert effect.reputation_delta == 0.0
        assert effect.popularity_delta == 0.0
        assert effect.stock_price_delta_percent == 0.0
        assert effect.satisfaction_delta == 0.0

    def test_create_event_effect_with_custom_values(self):
        """EventEffect acepta valores personalizados."""
        effect = EventEffect(
            reputation_delta=-10.0,
            popularity_delta=5.0,
            stock_price_delta_percent=-3.5,
            satisfaction_delta=2.0,
        )

        assert effect.reputation_delta == -10.0
        assert effect.popularity_delta == 5.0
        assert effect.stock_price_delta_percent == -3.5
        assert effect.satisfaction_delta == 2.0

    def test_event_effect_allows_negative_values(self):
        """EventEffect permite valores negativos para representar deterioro."""
        effect = EventEffect(
            reputation_delta=-50.0,
            popularity_delta=-20.0,
            stock_price_delta_percent=-15.0,
            satisfaction_delta=-10.0,
        )

        assert effect.reputation_delta == -50.0
        assert effect.popularity_delta == -20.0

    def test_event_effect_allows_positive_values(self):
        """EventEffect permite valores positivos para representar mejora."""
        effect = EventEffect(
            reputation_delta=25.0,
            popularity_delta=15.0,
            stock_price_delta_percent=10.0,
            satisfaction_delta=8.0,
        )

        assert effect.reputation_delta == 25.0
        assert effect.popularity_delta == 15.0

    def test_event_effect_is_immutable(self):
        """EventEffect es inmutable una vez creado."""
        effect = EventEffect(reputation_delta=10.0)

        with pytest.raises(ValidationError):
            effect.reputation_delta = 20.0

    def test_event_effect_serializes_to_json(self):
        """EventEffect se puede serializar a JSON."""
        effect = EventEffect(
            reputation_delta=-5.0,
            stock_price_delta_percent=-2.0,
        )

        json_str = effect.model_dump_json()
        data = json.loads(json_str)

        assert data["reputation_delta"] == -5.0
        assert data["stock_price_delta_percent"] == -2.0
        assert data["popularity_delta"] == 0.0
        assert data["satisfaction_delta"] == 0.0

    def test_event_effect_deserializes_from_json(self):
        """EventEffect se puede deserializar desde JSON."""
        json_str = '{"reputation_delta": 10.0, "popularity_delta": -5.0}'

        effect = EventEffect.model_validate_json(json_str)

        assert effect.reputation_delta == 10.0
        assert effect.popularity_delta == -5.0


class TestEvent:
    """Tests para la clase Event."""

    @pytest.fixture
    def sample_effect(self) -> EventEffect:
        """Fixture que proporciona un EventEffect de ejemplo."""
        return EventEffect(
            reputation_delta=-15.0,
            stock_price_delta_percent=-5.0,
        )

    def test_create_company_scandal_event(self, sample_effect: EventEffect):
        """Se puede crear un evento de escándalo de empresa."""
        event = Event(
            id="evt-001",
            day=5,
            event_type=EventType.COMPANY_SCANDAL,
            narrative="La empresa TechCorp sufre un escándalo de corrupción",
            target_company_ids=["tech-001"],
            effect=sample_effect,
        )

        assert event.id == "evt-001"
        assert event.day == 5
        assert event.event_type == EventType.COMPANY_SCANDAL
        assert event.narrative == "La empresa TechCorp sufre un escándalo de corrupción"
        assert event.target_company_ids == ["tech-001"]
        assert event.target_party_ids == []
        assert event.target_sectors == []
        assert event.effect.reputation_delta == -15.0

    def test_create_company_success_event(self):
        """Se puede crear un evento de éxito de empresa."""
        effect = EventEffect(
            reputation_delta=10.0,
            stock_price_delta_percent=8.0,
        )
        event = Event(
            id="evt-002",
            day=10,
            event_type=EventType.COMPANY_SUCCESS,
            narrative="FoodCorp lanza un producto revolucionario",
            target_company_ids=["food-001"],
            effect=effect,
        )

        assert event.event_type == EventType.COMPANY_SUCCESS
        assert event.effect.reputation_delta == 10.0

    def test_create_sector_crisis_event(self):
        """Se puede crear un evento de crisis sectorial."""
        effect = EventEffect(
            reputation_delta=-8.0,
            stock_price_delta_percent=-12.0,
            satisfaction_delta=-3.0,
        )
        event = Event(
            id="evt-003",
            day=15,
            event_type=EventType.SECTOR_CRISIS,
            narrative="El sector tecnológico enfrenta una crisis de suministros",
            target_sectors=[Sector.TECHNOLOGY],
            effect=effect,
        )

        assert event.event_type == EventType.SECTOR_CRISIS
        assert event.target_sectors == [Sector.TECHNOLOGY]
        assert event.target_company_ids == []

    def test_create_sector_boom_event(self):
        """Se puede crear un evento de boom sectorial."""
        effect = EventEffect(
            reputation_delta=5.0,
            stock_price_delta_percent=10.0,
            satisfaction_delta=2.0,
        )
        event = Event(
            id="evt-004",
            day=20,
            event_type=EventType.SECTOR_BOOM,
            narrative="El sector de la construcción experimenta un auge",
            target_sectors=[Sector.CONSTRUCTION, Sector.HOUSING],
            effect=effect,
        )

        assert event.event_type == EventType.SECTOR_BOOM
        assert len(event.target_sectors) == 2
        assert Sector.CONSTRUCTION in event.target_sectors
        assert Sector.HOUSING in event.target_sectors

    def test_create_party_scandal_event(self):
        """Se puede crear un evento de escándalo de partido."""
        effect = EventEffect(
            reputation_delta=-20.0,
            popularity_delta=-10.0,
        )
        event = Event(
            id="evt-005",
            day=25,
            event_type=EventType.PARTY_SCANDAL,
            narrative="Se destapa un caso de corrupción en el Partido Progresista",
            target_party_ids=["party-001"],
            effect=effect,
        )

        assert event.event_type == EventType.PARTY_SCANDAL
        assert event.target_party_ids == ["party-001"]
        assert event.effect.popularity_delta == -10.0

    def test_create_party_success_event(self):
        """Se puede crear un evento de éxito de partido."""
        effect = EventEffect(
            reputation_delta=15.0,
            popularity_delta=8.0,
        )
        event = Event(
            id="evt-006",
            day=30,
            event_type=EventType.PARTY_SUCCESS,
            narrative="El Partido Conservador logra un acuerdo histórico",
            target_party_ids=["party-002"],
            effect=effect,
        )

        assert event.event_type == EventType.PARTY_SUCCESS
        assert event.effect.popularity_delta == 8.0

    def test_create_policy_proposal_event(self):
        """Se puede crear un evento de propuesta de política."""
        effect = EventEffect(
            popularity_delta=3.0,
            satisfaction_delta=1.0,
        )
        event = Event(
            id="evt-007",
            day=35,
            event_type=EventType.POLICY_PROPOSAL,
            narrative="El gobierno propone una nueva ley de vivienda",
            target_party_ids=["party-001"],
            target_sectors=[Sector.HOUSING],
            effect=effect,
        )

        assert event.event_type == EventType.POLICY_PROPOSAL
        assert event.target_party_ids == ["party-001"]
        assert event.target_sectors == [Sector.HOUSING]

    def test_event_requires_id(self, sample_effect: EventEffect):
        """Event requiere un id."""
        with pytest.raises(ValidationError) as exc_info:
            Event(
                day=1,
                event_type=EventType.COMPANY_SCANDAL,
                narrative="Test",
                effect=sample_effect,
            )
        assert "id" in str(exc_info.value)

    def test_event_requires_day(self, sample_effect: EventEffect):
        """Event requiere un día."""
        with pytest.raises(ValidationError) as exc_info:
            Event(
                id="evt-001",
                event_type=EventType.COMPANY_SCANDAL,
                narrative="Test",
                effect=sample_effect,
            )
        assert "day" in str(exc_info.value)

    def test_event_requires_event_type(self, sample_effect: EventEffect):
        """Event requiere un tipo de evento."""
        with pytest.raises(ValidationError) as exc_info:
            Event(
                id="evt-001",
                day=1,
                narrative="Test",
                effect=sample_effect,
            )
        assert "event_type" in str(exc_info.value)

    def test_event_requires_narrative(self, sample_effect: EventEffect):
        """Event requiere una narrativa."""
        with pytest.raises(ValidationError) as exc_info:
            Event(
                id="evt-001",
                day=1,
                event_type=EventType.COMPANY_SCANDAL,
                effect=sample_effect,
            )
        assert "narrative" in str(exc_info.value)

    def test_event_requires_effect(self):
        """Event requiere un efecto."""
        with pytest.raises(ValidationError) as exc_info:
            Event(
                id="evt-001",
                day=1,
                event_type=EventType.COMPANY_SCANDAL,
                narrative="Test",
            )
        assert "effect" in str(exc_info.value)

    def test_event_day_cannot_be_negative(self, sample_effect: EventEffect):
        """El día del evento no puede ser negativo."""
        with pytest.raises(ValidationError) as exc_info:
            Event(
                id="evt-001",
                day=-1,
                event_type=EventType.COMPANY_SCANDAL,
                narrative="Test",
                effect=sample_effect,
            )
        assert "day" in str(exc_info.value)

    def test_event_is_immutable(self, sample_effect: EventEffect):
        """Event es inmutable una vez creado."""
        event = Event(
            id="evt-001",
            day=1,
            event_type=EventType.COMPANY_SCANDAL,
            narrative="Test",
            effect=sample_effect,
        )

        with pytest.raises(ValidationError):
            event.day = 2

    def test_event_serializes_to_json(self, sample_effect: EventEffect):
        """Event se puede serializar a JSON."""
        event = Event(
            id="evt-001",
            day=5,
            event_type=EventType.SECTOR_CRISIS,
            narrative="Crisis en el sector tecnológico",
            target_sectors=[Sector.TECHNOLOGY],
            effect=sample_effect,
        )

        json_str = event.model_dump_json()
        data = json.loads(json_str)

        assert data["id"] == "evt-001"
        assert data["day"] == 5
        assert data["event_type"] == "sector_crisis"
        assert data["narrative"] == "Crisis en el sector tecnológico"
        assert data["target_sectors"] == ["technology"]
        assert data["effect"]["reputation_delta"] == -15.0

    def test_event_deserializes_from_json(self):
        """Event se puede deserializar desde JSON."""
        json_str = """
        {
            "id": "evt-002",
            "day": 10,
            "event_type": "company_success",
            "narrative": "Éxito empresarial",
            "target_company_ids": ["comp-001"],
            "target_party_ids": [],
            "target_sectors": [],
            "effect": {
                "reputation_delta": 10.0,
                "popularity_delta": 0.0,
                "stock_price_delta_percent": 5.0,
                "satisfaction_delta": 0.0
            }
        }
        """

        event = Event.model_validate_json(json_str)

        assert event.id == "evt-002"
        assert event.day == 10
        assert event.event_type == EventType.COMPANY_SUCCESS
        assert event.target_company_ids == ["comp-001"]
        assert event.effect.reputation_delta == 10.0
        assert event.effect.stock_price_delta_percent == 5.0

    def test_event_with_multiple_targets(self):
        """Event puede tener múltiples objetivos de diferentes tipos."""
        effect = EventEffect(reputation_delta=-5.0)
        event = Event(
            id="evt-008",
            day=40,
            event_type=EventType.SECTOR_CRISIS,
            narrative="Crisis económica global afecta múltiples sectores",
            target_company_ids=["comp-001", "comp-002"],
            target_party_ids=["party-001"],
            target_sectors=[Sector.FINANCE, Sector.TECHNOLOGY],
            effect=effect,
        )

        assert len(event.target_company_ids) == 2
        assert len(event.target_party_ids) == 1
        assert len(event.target_sectors) == 2

