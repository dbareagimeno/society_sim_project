"""
Tests para la fase de registro de resumen diario.

Verifica el funcionamiento de _record_summary_phase y la correcta
generación de DaySummary con todas las métricas calculadas.
"""

import pytest

from society_sim.domain import (
    CitizenSegment,
    Company,
    DaySummary,
    IdeologicalBias,
    Party,
    Sector,
    WorldState,
    create_initial_world,
)
from society_sim.engine import run_day


class TestRecordSummaryPhaseBasic:
    """Tests básicos de la fase de registro de resumen."""

    def test_history_grows_with_each_day(self):
        """Verifica que el histórico crece con cada día simulado."""
        world = create_initial_world()
        assert len(world.history) == 0

        world = run_day(world)
        assert len(world.history) == 1

        world = run_day(world)
        assert len(world.history) == 2

        world = run_day(world)
        assert len(world.history) == 3

    def test_summary_day_matches_world_day(self):
        """Verifica que el día del resumen coincide con el día del mundo."""
        world = create_initial_world()
        
        # Simular varios días
        for expected_day in range(5):
            # El resumen se registra antes de incrementar el día
            world = run_day(world)
            # El resumen del día N se registra cuando world.day pasa de N a N+1
            assert world.history[expected_day].day == expected_day

    def test_summary_is_day_summary_instance(self):
        """Verifica que cada elemento del histórico es un DaySummary."""
        world = create_initial_world()
        world = run_day(world)

        assert len(world.history) == 1
        assert isinstance(world.history[0], DaySummary)


class TestRecordSummaryMetrics:
    """Tests de cálculo de métricas agregadas."""

    @pytest.fixture
    def world_with_revenue(self):
        """Crea un mundo con empresas que tienen revenue específico."""
        companies = [
            Company(
                id="company-1",
                name="Company 1",
                sector=Sector.TECHNOLOGY,
                base_quality=0.7,
                base_price_level=0.5,
                stock_price=100.0,
                last_day_revenue=1000.0,
            ),
            Company(
                id="company-2",
                name="Company 2",
                sector=Sector.FOOD,
                base_quality=0.6,
                base_price_level=0.4,
                stock_price=200.0,
                last_day_revenue=2000.0,
            ),
            Company(
                id="company-3",
                name="Company 3",
                sector=Sector.HEALTHCARE,
                base_quality=0.8,
                base_price_level=0.6,
                stock_price=150.0,
                last_day_revenue=1500.0,
            ),
        ]
        party = Party(
            id="test-party",
            name="Test Party",
            ideology=IdeologicalBias.CENTER,
            popularity=60.0,
            reputation=70.0,
        )
        segment = CitizenSegment(
            id="test-segment",
            name="Test Segment",
            size=1000,
            wealth_per_capita=10000.0,
            ideological_bias=IdeologicalBias.CENTER,
            satisfaction=75.0,
        )
        return WorldState(
            companies=companies,
            parties=[party],
            citizen_segments=[segment],
        )

    def test_total_revenue_is_sum_of_company_revenues(self, world_with_revenue):
        """Verifica que total_revenue es la suma de ingresos de todas las empresas."""
        world = run_day(world_with_revenue)
        summary = world.history[0]

        # 1000 + 2000 + 1500 = 4500
        assert summary.total_revenue == 4500.0

    def test_average_stock_price_is_mean_of_prices(self, world_with_revenue):
        """Verifica que average_stock_price es la media de precios de acciones."""
        world = run_day(world_with_revenue)
        summary = world.history[0]

        # (100 + 200 + 150) / 3 = 150
        assert summary.average_stock_price == 150.0

    def test_average_satisfaction_is_weighted_by_size(self):
        """Verifica que average_satisfaction es la media ponderada por tamaño."""
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
        # Dos segmentos con diferentes tamaños y satisfacciones
        segment1 = CitizenSegment(
            id="segment-1",
            name="Small Segment",
            size=100,
            wealth_per_capita=10000.0,
            ideological_bias=IdeologicalBias.CENTER,
            satisfaction=80.0,
        )
        segment2 = CitizenSegment(
            id="segment-2",
            name="Large Segment",
            size=400,
            wealth_per_capita=5000.0,
            ideological_bias=IdeologicalBias.CENTER,
            satisfaction=60.0,
        )
        world = WorldState(
            companies=[company],
            parties=[party],
            citizen_segments=[segment1, segment2],
        )

        world = run_day(world)
        summary = world.history[0]

        # Media ponderada: (80*100 + 60*400) / (100 + 400) = (8000 + 24000) / 500 = 64
        assert summary.average_satisfaction == 64.0


class TestPartySummaries:
    """Tests de creación de resúmenes de partidos."""

    def test_party_summaries_created_for_all_parties(self):
        """Verifica que se crea un PartySummary para cada partido."""
        company = Company(
            id="test-company",
            name="Test Corp",
            sector=Sector.TECHNOLOGY,
            base_quality=0.7,
            base_price_level=0.5,
        )
        parties = [
            Party(
                id=f"party-{i}",
                name=f"Party {i}",
                ideology=IdeologicalBias.CENTER,
                popularity=20.0 + i * 10,
                reputation=50.0 + i * 5,
            )
            for i in range(3)
        ]
        segment = CitizenSegment(
            id="test-segment",
            name="Test Segment",
            size=1000,
            wealth_per_capita=10000.0,
            ideological_bias=IdeologicalBias.CENTER,
        )
        world = WorldState(
            companies=[company],
            parties=parties,
            citizen_segments=[segment],
        )

        world = run_day(world)
        summary = world.history[0]

        assert len(summary.parties) == 3

        for i, party_summary in enumerate(summary.parties):
            assert party_summary.party_id == f"party-{i}"
            assert party_summary.name == f"Party {i}"
            assert party_summary.popularity == 20.0 + i * 10
            assert party_summary.reputation == 50.0 + i * 5


class TestCompanySummaries:
    """Tests de creación de resúmenes de empresas."""

    def test_top_companies_limited_to_5(self):
        """Verifica que top_companies se limita a las 5 mejores por revenue."""
        companies = [
            Company(
                id=f"company-{i}",
                name=f"Company {i}",
                sector=Sector.TECHNOLOGY,
                base_quality=0.7,
                base_price_level=0.5,
                last_day_revenue=float(i * 100),
            )
            for i in range(10)
        ]
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
        world = WorldState(
            companies=companies,
            parties=[party],
            citizen_segments=[segment],
        )

        world = run_day(world)
        summary = world.history[0]

        assert len(summary.top_companies) == 5

    def test_top_companies_sorted_by_revenue_descending(self):
        """Verifica que top_companies está ordenado por revenue descendente."""
        companies = [
            Company(
                id="low",
                name="Low Revenue Co",
                sector=Sector.TECHNOLOGY,
                base_quality=0.7,
                base_price_level=0.5,
                last_day_revenue=100.0,
            ),
            Company(
                id="high",
                name="High Revenue Co",
                sector=Sector.FOOD,
                base_quality=0.6,
                base_price_level=0.4,
                last_day_revenue=5000.0,
            ),
            Company(
                id="medium",
                name="Medium Revenue Co",
                sector=Sector.HEALTHCARE,
                base_quality=0.8,
                base_price_level=0.6,
                last_day_revenue=1000.0,
            ),
        ]
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
        world = WorldState(
            companies=companies,
            parties=[party],
            citizen_segments=[segment],
        )

        world = run_day(world)
        summary = world.history[0]

        # Las empresas deben estar ordenadas por revenue descendente
        assert summary.top_companies[0].company_id == "high"
        assert summary.top_companies[0].revenue == 5000.0
        assert summary.top_companies[1].company_id == "medium"
        assert summary.top_companies[1].revenue == 1000.0
        assert summary.top_companies[2].company_id == "low"
        assert summary.top_companies[2].revenue == 100.0

    def test_company_summary_includes_all_fields(self):
        """Verifica que CompanySummary incluye todos los campos correctos."""
        company = Company(
            id="test-company",
            name="Test Corp",
            sector=Sector.TECHNOLOGY,
            base_quality=0.7,
            base_price_level=0.5,
            stock_price=150.0,
            reputation=85.0,
            last_day_revenue=2500.0,
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
        world = WorldState(
            companies=[company],
            parties=[party],
            citizen_segments=[segment],
        )

        world = run_day(world)
        company_summary = world.history[0].top_companies[0]

        assert company_summary.company_id == "test-company"
        assert company_summary.name == "Test Corp"
        assert company_summary.stock_price == 150.0
        assert company_summary.reputation == 85.0
        assert company_summary.revenue == 2500.0


class TestSummaryEventAndPolicyCount:
    """Tests de conteo de eventos y políticas."""

    def test_events_count_is_zero_initially(self):
        """Verifica que events_count es 0 cuando no hay eventos."""
        world = create_initial_world()
        world = run_day(world)

        assert world.history[0].events_count == 0

    def test_active_policies_count_is_zero_initially(self):
        """Verifica que active_policies_count es 0 cuando no hay políticas."""
        world = create_initial_world()
        world = run_day(world)

        assert world.history[0].active_policies_count == 0


class TestMultipleDaysSummary:
    """Tests de ejecución de múltiples días con resumen."""

    def test_multiple_days_builds_complete_history(self):
        """Verifica que ejecutar múltiples días construye un historial completo."""
        world = create_initial_world()

        # Simular 10 días
        for _ in range(10):
            world = run_day(world)

        assert len(world.history) == 10
        
        # Verificar que cada día tiene su resumen correspondiente
        for i, summary in enumerate(world.history):
            assert summary.day == i

    def test_history_is_immutable_snapshot(self):
        """Verifica que cada resumen es una instantánea inmutable del día."""
        world = create_initial_world()
        
        world = run_day(world)
        first_summary = world.history[0]
        
        world = run_day(world)
        
        # El primer resumen no debe cambiar
        assert world.history[0] == first_summary
        assert world.history[0] is first_summary

