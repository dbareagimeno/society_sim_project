"""
Tests para el motor de simulación diaria.

Verifica el funcionamiento básico de run_day y la estructura de fases.
"""

import pytest

from society_sim.domain import (
    CitizenSegment,
    Company,
    IdeologicalBias,
    Party,
    Sector,
    WorldState,
    create_initial_world,
)
from society_sim.engine import run_day


class TestRunDayBasic:
    """Tests básicos de la función run_day."""

    def test_run_day_increments_day_counter(self):
        """Verifica que run_day incrementa el contador de día en 1."""
        world = create_initial_world()
        assert world.day == 0

        new_world = run_day(world)

        assert new_world.day == 1

    def test_run_day_preserves_companies(self):
        """Verifica que run_day preserva la lista de empresas."""
        world = create_initial_world()
        initial_company_count = len(world.companies)
        initial_company_ids = {c.id for c in world.companies}

        new_world = run_day(world)

        assert len(new_world.companies) == initial_company_count
        assert {c.id for c in new_world.companies} == initial_company_ids

    def test_run_day_preserves_parties(self):
        """Verifica que run_day preserva la lista de partidos."""
        world = create_initial_world()
        initial_party_count = len(world.parties)
        initial_party_ids = {p.id for p in world.parties}

        new_world = run_day(world)

        assert len(new_world.parties) == initial_party_count
        assert {p.id for p in new_world.parties} == initial_party_ids

    def test_run_day_preserves_citizen_segments(self):
        """Verifica que run_day preserva los segmentos ciudadanos."""
        world = create_initial_world()
        initial_segment_count = len(world.citizen_segments)
        initial_segment_ids = {s.id for s in world.citizen_segments}

        new_world = run_day(world)

        assert len(new_world.citizen_segments) == initial_segment_count
        assert {s.id for s in new_world.citizen_segments} == initial_segment_ids

    def test_run_day_clears_events_today(self):
        """Verifica que run_day limpia los eventos del día anterior."""
        world = create_initial_world()
        # Aunque no hay eventos, verificamos que events_today existe y está vacío
        new_world = run_day(world)

        assert new_world.events_today == []


class TestRunDayMultipleDays:
    """Tests de ejecución de múltiples días."""

    def test_run_multiple_days_increments_correctly(self):
        """Verifica que ejecutar varios días incrementa el contador correctamente."""
        world = create_initial_world()
        assert world.day == 0

        # Simular 10 días
        for expected_day in range(1, 11):
            world = run_day(world)
            assert world.day == expected_day

    def test_run_day_returns_new_world_state(self):
        """Verifica que run_day retorna un nuevo WorldState (inmutabilidad)."""
        world = create_initial_world()
        new_world = run_day(world)

        # El mundo original no debe modificarse
        assert world.day == 0
        assert new_world.day == 1
        assert world is not new_world


class TestRunDayWithMinimalWorld:
    """Tests con un WorldState mínimo creado manualmente."""

    @pytest.fixture
    def minimal_world(self):
        """Crea un WorldState mínimo para testing."""
        company = Company(
            id="test-company",
            name="Test Corp",
            sector=Sector.TECHNOLOGY,
            base_quality=0.7,
            base_price_level=0.5,
        )
        party = Party(
            id="test-party",
            name="Test Party",
            ideology=IdeologicalBias.CENTER,
        )
        segment = CitizenSegment(
            id="test-segment",
            name="Test Segment",
            size=1000,
            wealth_per_capita=10000.0,
            ideological_bias=IdeologicalBias.CENTER,
        )
        return WorldState(
            companies=[company],
            parties=[party],
            citizen_segments=[segment],
        )

    def test_run_day_with_minimal_world(self, minimal_world):
        """Verifica que run_day funciona con un mundo mínimo."""
        assert minimal_world.day == 0

        new_world = run_day(minimal_world)

        assert new_world.day == 1
        assert len(new_world.companies) == 1
        assert len(new_world.parties) == 1
        assert len(new_world.citizen_segments) == 1

    def test_run_day_preserves_world_validity(self, minimal_world):
        """Verifica que el mundo sigue siendo válido después de run_day."""
        new_world = run_day(minimal_world)

        # Si llegamos aquí sin excepción, el mundo es válido
        # (WorldState tiene validadores que verifican entidades mínimas)
        assert new_world is not None
        assert isinstance(new_world, WorldState)


class TestRunDayImport:
    """Tests de importación correcta."""

    def test_run_day_importable_from_engine(self):
        """Verifica que run_day es importable desde society_sim.engine."""
        from society_sim.engine import run_day as imported_run_day

        assert callable(imported_run_day)

    def test_run_day_in_engine_all(self):
        """Verifica que run_day está en __all__ del módulo engine."""
        import society_sim.engine as engine_module

        assert "run_day" in engine_module.__all__

