"""
Tests unitarios para el modelo WorldState.

Verifica:
- Creación de WorldState válido
- Validación de mínimo de entidades requeridas
- Funcionamiento de métodos helper
- Serialización/deserialización a JSON
"""

import json

import pytest
from pydantic import ValidationError

from society_sim.domain import (
    CitizenSegment,
    Company,
    DaySummary,
    Event,
    EventEffect,
    EventType,
    IdeologicalBias,
    Party,
    Policy,
    PolicyEffect,
    Sector,
)
from society_sim.domain.world_state import WorldState


# Fixtures para crear entidades de prueba
@pytest.fixture
def sample_company() -> Company:
    """Crea una empresa de prueba."""
    return Company(
        id="tech-001",
        name="TechCorp",
        sector=Sector.TECHNOLOGY,
        base_quality=0.8,
        base_price_level=0.6,
    )


@pytest.fixture
def sample_company_food() -> Company:
    """Crea una empresa del sector alimentación."""
    return Company(
        id="food-001",
        name="FoodMart",
        sector=Sector.FOOD,
        base_quality=0.7,
        base_price_level=0.4,
    )


@pytest.fixture
def sample_company_tech2() -> Company:
    """Crea una segunda empresa de tecnología."""
    return Company(
        id="tech-002",
        name="TechStartup",
        sector=Sector.TECHNOLOGY,
        base_quality=0.6,
        base_price_level=0.5,
    )


@pytest.fixture
def sample_party() -> Party:
    """Crea un partido político de prueba."""
    return Party(
        id="prog-001",
        name="Partido Progresista",
        ideology=IdeologicalBias.CENTER_LEFT,
    )


@pytest.fixture
def sample_party_2() -> Party:
    """Crea un segundo partido político."""
    return Party(
        id="cons-001",
        name="Partido Conservador",
        ideology=IdeologicalBias.CENTER_RIGHT,
        in_government=True,
    )


@pytest.fixture
def sample_segment() -> CitizenSegment:
    """Crea un segmento ciudadano de prueba."""
    return CitizenSegment(
        id="middle-class",
        name="Clase Media",
        size=1_000_000,
        wealth_per_capita=50_000.0,
        ideological_bias=IdeologicalBias.CENTER,
    )


@pytest.fixture
def sample_segment_2() -> CitizenSegment:
    """Crea un segundo segmento ciudadano."""
    return CitizenSegment(
        id="working-class",
        name="Clase Trabajadora",
        size=2_000_000,
        wealth_per_capita=25_000.0,
        ideological_bias=IdeologicalBias.CENTER_LEFT,
    )


@pytest.fixture
def sample_policy(sample_party: Party) -> Policy:
    """Crea una política de prueba."""
    return Policy(
        id="pol-001",
        name="Subsidio Tecnológico",
        description="Subsidios para empresas de tecnología",
        proposed_by_party_id=sample_party.id,
        effect=PolicyEffect(
            target_sector=Sector.TECHNOLOGY,
            subsidy_amount=10000.0,
        ),
        duration_days=30,
        remaining_days=30,
    )


@pytest.fixture
def sample_event() -> Event:
    """Crea un evento de prueba."""
    return Event(
        id="evt-001",
        day=1,
        event_type=EventType.COMPANY_SUCCESS,
        narrative="TechCorp lanza un producto innovador",
        target_company_ids=["tech-001"],
        effect=EventEffect(reputation_delta=5.0, stock_price_delta_percent=3.0),
    )


@pytest.fixture
def sample_day_summary() -> DaySummary:
    """Crea un resumen de día de prueba."""
    return DaySummary(
        day=0,
        total_revenue=100000.0,
        average_stock_price=100.0,
        average_satisfaction=50.0,
        events_count=1,
        active_policies_count=0,
    )


@pytest.fixture
def minimal_world(
    sample_company: Company,
    sample_party: Party,
    sample_segment: CitizenSegment,
) -> WorldState:
    """Crea un WorldState mínimo válido."""
    return WorldState(
        companies=[sample_company],
        parties=[sample_party],
        citizen_segments=[sample_segment],
    )


class TestWorldStateCreation:
    """Tests de creación de WorldState válido."""

    def test_create_minimal_world_state(
        self,
        sample_company: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe crear un WorldState con los campos mínimos requeridos."""
        world = WorldState(
            companies=[sample_company],
            parties=[sample_party],
            citizen_segments=[sample_segment],
        )

        assert len(world.companies) == 1
        assert len(world.parties) == 1
        assert len(world.citizen_segments) == 1

    def test_create_world_state_has_default_values(
        self,
        sample_company: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe asignar valores por defecto a campos opcionales."""
        world = WorldState(
            companies=[sample_company],
            parties=[sample_party],
            citizen_segments=[sample_segment],
        )

        assert world.day == 0
        assert world.active_policies == []
        assert world.events_today == []
        assert world.history == []

    def test_create_world_state_with_custom_day(
        self,
        sample_company: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe permitir inicializar con un día específico."""
        world = WorldState(
            day=10,
            companies=[sample_company],
            parties=[sample_party],
            citizen_segments=[sample_segment],
        )

        assert world.day == 10

    def test_create_world_state_with_policies(
        self,
        sample_company: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
        sample_policy: Policy,
    ) -> None:
        """Debe poder crear WorldState con políticas activas."""
        world = WorldState(
            companies=[sample_company],
            parties=[sample_party],
            citizen_segments=[sample_segment],
            active_policies=[sample_policy],
        )

        assert len(world.active_policies) == 1
        assert world.active_policies[0].id == "pol-001"

    def test_create_world_state_with_events(
        self,
        sample_company: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
        sample_event: Event,
    ) -> None:
        """Debe poder crear WorldState con eventos del día."""
        world = WorldState(
            companies=[sample_company],
            parties=[sample_party],
            citizen_segments=[sample_segment],
            events_today=[sample_event],
        )

        assert len(world.events_today) == 1
        assert world.events_today[0].id == "evt-001"

    def test_create_world_state_with_history(
        self,
        sample_company: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
        sample_day_summary: DaySummary,
    ) -> None:
        """Debe poder crear WorldState con historial."""
        world = WorldState(
            companies=[sample_company],
            parties=[sample_party],
            citizen_segments=[sample_segment],
            history=[sample_day_summary],
        )

        assert len(world.history) == 1
        assert world.history[0].day == 0

    def test_create_world_state_with_multiple_entities(
        self,
        sample_company: Company,
        sample_company_food: Company,
        sample_company_tech2: Company,
        sample_party: Party,
        sample_party_2: Party,
        sample_segment: CitizenSegment,
        sample_segment_2: CitizenSegment,
    ) -> None:
        """Debe poder crear WorldState con múltiples entidades."""
        world = WorldState(
            companies=[sample_company, sample_company_food, sample_company_tech2],
            parties=[sample_party, sample_party_2],
            citizen_segments=[sample_segment, sample_segment_2],
        )

        assert len(world.companies) == 3
        assert len(world.parties) == 2
        assert len(world.citizen_segments) == 2


class TestWorldStateValidation:
    """Tests de validación de WorldState."""

    def test_empty_companies_raises_error(
        self,
        sample_party: Party,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe lanzar error si no hay empresas."""
        with pytest.raises(ValidationError) as exc_info:
            WorldState(
                companies=[],
                parties=[sample_party],
                citizen_segments=[sample_segment],
            )
        assert "al menos 1 empresa" in str(exc_info.value)

    def test_empty_parties_raises_error(
        self,
        sample_company: Company,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe lanzar error si no hay partidos."""
        with pytest.raises(ValidationError) as exc_info:
            WorldState(
                companies=[sample_company],
                parties=[],
                citizen_segments=[sample_segment],
            )
        assert "al menos 1 partido" in str(exc_info.value)

    def test_empty_segments_raises_error(
        self,
        sample_company: Company,
        sample_party: Party,
    ) -> None:
        """Debe lanzar error si no hay segmentos ciudadanos."""
        with pytest.raises(ValidationError) as exc_info:
            WorldState(
                companies=[sample_company],
                parties=[sample_party],
                citizen_segments=[],
            )
        assert "al menos 1 segmento" in str(exc_info.value)

    def test_negative_day_raises_error(
        self,
        sample_company: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe lanzar error si el día es negativo."""
        with pytest.raises(ValidationError) as exc_info:
            WorldState(
                day=-1,
                companies=[sample_company],
                parties=[sample_party],
                citizen_segments=[sample_segment],
            )
        assert "day" in str(exc_info.value)


class TestWorldStateHelperMethods:
    """Tests de los métodos helper de WorldState."""

    def test_get_company_by_id_found(self, minimal_world: WorldState) -> None:
        """Debe encontrar una empresa existente por ID."""
        company = minimal_world.get_company_by_id("tech-001")

        assert company is not None
        assert company.id == "tech-001"
        assert company.name == "TechCorp"

    def test_get_company_by_id_not_found(self, minimal_world: WorldState) -> None:
        """Debe retornar None si la empresa no existe."""
        company = minimal_world.get_company_by_id("nonexistent")

        assert company is None

    def test_get_party_by_id_found(self, minimal_world: WorldState) -> None:
        """Debe encontrar un partido existente por ID."""
        party = minimal_world.get_party_by_id("prog-001")

        assert party is not None
        assert party.id == "prog-001"
        assert party.name == "Partido Progresista"

    def test_get_party_by_id_not_found(self, minimal_world: WorldState) -> None:
        """Debe retornar None si el partido no existe."""
        party = minimal_world.get_party_by_id("nonexistent")

        assert party is None

    def test_get_segment_by_id_found(self, minimal_world: WorldState) -> None:
        """Debe encontrar un segmento existente por ID."""
        segment = minimal_world.get_segment_by_id("middle-class")

        assert segment is not None
        assert segment.id == "middle-class"
        assert segment.name == "Clase Media"

    def test_get_segment_by_id_not_found(self, minimal_world: WorldState) -> None:
        """Debe retornar None si el segmento no existe."""
        segment = minimal_world.get_segment_by_id("nonexistent")

        assert segment is None

    def test_get_companies_by_sector_found(
        self,
        sample_company: Company,
        sample_company_food: Company,
        sample_company_tech2: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe encontrar empresas del sector especificado."""
        world = WorldState(
            companies=[sample_company, sample_company_food, sample_company_tech2],
            parties=[sample_party],
            citizen_segments=[sample_segment],
        )

        tech_companies = world.get_companies_by_sector(Sector.TECHNOLOGY)

        assert len(tech_companies) == 2
        assert all(c.sector == Sector.TECHNOLOGY for c in tech_companies)

    def test_get_companies_by_sector_single(
        self,
        sample_company: Company,
        sample_company_food: Company,
        sample_party: Party,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe encontrar una sola empresa del sector."""
        world = WorldState(
            companies=[sample_company, sample_company_food],
            parties=[sample_party],
            citizen_segments=[sample_segment],
        )

        food_companies = world.get_companies_by_sector(Sector.FOOD)

        assert len(food_companies) == 1
        assert food_companies[0].id == "food-001"

    def test_get_companies_by_sector_empty(self, minimal_world: WorldState) -> None:
        """Debe retornar lista vacía si no hay empresas del sector."""
        companies = minimal_world.get_companies_by_sector(Sector.HEALTHCARE)

        assert companies == []

    def test_get_companies_by_sector_all_sectors(
        self,
        sample_party: Party,
        sample_segment: CitizenSegment,
    ) -> None:
        """Debe funcionar para todos los sectores."""
        companies = []
        for sector in Sector:
            companies.append(
                Company(
                    id=f"{sector.value}-001",
                    name=f"Company in {sector.value}",
                    sector=sector,
                    base_quality=0.5,
                    base_price_level=0.5,
                )
            )

        world = WorldState(
            companies=companies,
            parties=[sample_party],
            citizen_segments=[sample_segment],
        )

        for sector in Sector:
            sector_companies = world.get_companies_by_sector(sector)
            assert len(sector_companies) == 1
            assert sector_companies[0].sector == sector


class TestWorldStateSerialization:
    """Tests de serialización y deserialización JSON."""

    def test_serialize_to_json(self, minimal_world: WorldState) -> None:
        """Debe poder serializar un WorldState a JSON."""
        json_str = minimal_world.model_dump_json()
        data = json.loads(json_str)

        assert data["day"] == 0
        assert len(data["companies"]) == 1
        assert len(data["parties"]) == 1
        assert len(data["citizen_segments"]) == 1
        assert data["active_policies"] == []
        assert data["events_today"] == []
        assert data["history"] == []

    def test_deserialize_from_json(self) -> None:
        """Debe poder deserializar un WorldState desde JSON."""
        json_data = {
            "day": 5,
            "companies": [
                {
                    "id": "tech-001",
                    "name": "TechCorp",
                    "sector": "technology",
                    "base_quality": 0.8,
                    "base_price_level": 0.6,
                }
            ],
            "parties": [
                {
                    "id": "prog-001",
                    "name": "Partido Progresista",
                    "ideology": "center_left",
                }
            ],
            "citizen_segments": [
                {
                    "id": "middle-class",
                    "name": "Clase Media",
                    "size": 1000000,
                    "wealth_per_capita": 50000.0,
                    "ideological_bias": "center",
                }
            ],
        }

        world = WorldState.model_validate(json_data)

        assert world.day == 5
        assert len(world.companies) == 1
        assert world.companies[0].name == "TechCorp"

    def test_roundtrip_serialization(
        self,
        sample_company: Company,
        sample_company_food: Company,
        sample_party: Party,
        sample_party_2: Party,
        sample_segment: CitizenSegment,
        sample_policy: Policy,
        sample_event: Event,
        sample_day_summary: DaySummary,
    ) -> None:
        """Debe mantener los datos tras serializar y deserializar."""
        original = WorldState(
            day=10,
            companies=[sample_company, sample_company_food],
            parties=[sample_party, sample_party_2],
            citizen_segments=[sample_segment],
            active_policies=[sample_policy],
            events_today=[sample_event],
            history=[sample_day_summary],
        )

        # Serializar y deserializar
        json_str = original.model_dump_json()
        restored = WorldState.model_validate_json(json_str)

        assert restored.day == original.day
        assert len(restored.companies) == len(original.companies)
        assert len(restored.parties) == len(original.parties)
        assert len(restored.citizen_segments) == len(original.citizen_segments)
        assert len(restored.active_policies) == len(original.active_policies)
        assert len(restored.events_today) == len(original.events_today)
        assert len(restored.history) == len(original.history)

        # Verificar integridad de datos
        assert restored.companies[0].id == original.companies[0].id
        assert restored.parties[0].name == original.parties[0].name
        assert restored.active_policies[0].name == original.active_policies[0].name


class TestWorldStateModelCopy:
    """Tests de model_copy para actualizaciones inmutables."""

    def test_model_copy_update_day(self, minimal_world: WorldState) -> None:
        """Debe poder crear copia con día actualizado."""
        updated = minimal_world.model_copy(update={"day": minimal_world.day + 1})

        assert updated.day == 1
        assert minimal_world.day == 0  # Original sin cambios

    def test_model_copy_preserves_references(self, minimal_world: WorldState) -> None:
        """Las copias deben preservar las referencias a entidades."""
        updated = minimal_world.model_copy(update={"day": 5})

        assert updated.companies == minimal_world.companies
        assert updated.parties == minimal_world.parties
        assert updated.citizen_segments == minimal_world.citizen_segments

    def test_model_copy_with_new_events(
        self,
        minimal_world: WorldState,
        sample_event: Event,
    ) -> None:
        """Debe poder crear copia con nuevos eventos."""
        updated = minimal_world.model_copy(update={"events_today": [sample_event]})

        assert len(updated.events_today) == 1
        assert len(minimal_world.events_today) == 0  # Original sin cambios

