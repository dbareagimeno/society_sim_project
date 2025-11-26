"""
Tests de imports del módulo domain para SocietySim.

Verifica que todos los modelos y funciones sean importables desde
society_sim.domain sin imports circulares.
"""


class TestDomainImports:
    """Tests para verificar que todos los exports del módulo domain funcionan."""

    def test_import_all_from_domain(self) -> None:
        """Verifica que se pueden importar todos los exports desde society_sim.domain."""
        from society_sim.domain import (
            CitizenSegment,
            Company,
            CompanySummary,
            DaySummary,
            Event,
            EventEffect,
            EventType,
            IdeologicalBias,
            Party,
            PartySummary,
            Policy,
            PolicyEffect,
            Sector,
            WorldState,
            create_initial_world,
        )

        # Verificar que los imports son los tipos correctos
        assert CitizenSegment is not None
        assert Company is not None
        assert CompanySummary is not None
        assert DaySummary is not None
        assert Event is not None
        assert EventEffect is not None
        assert EventType is not None
        assert IdeologicalBias is not None
        assert Party is not None
        assert PartySummary is not None
        assert Policy is not None
        assert PolicyEffect is not None
        assert Sector is not None
        assert WorldState is not None
        assert create_initial_world is not None

    def test_enums_are_importable(self) -> None:
        """Verifica que los enums son importables y tienen los valores esperados."""
        from society_sim.domain import EventType, IdeologicalBias, Sector

        # Sector
        assert Sector.HOUSING == "housing"
        assert Sector.FOOD == "food"
        assert Sector.TECHNOLOGY == "technology"
        assert Sector.CONSTRUCTION == "construction"
        assert Sector.HEALTHCARE == "healthcare"
        assert Sector.FINANCE == "finance"

        # EventType
        assert EventType.COMPANY_SCANDAL == "company_scandal"
        assert EventType.COMPANY_SUCCESS == "company_success"
        assert EventType.SECTOR_CRISIS == "sector_crisis"
        assert EventType.SECTOR_BOOM == "sector_boom"
        assert EventType.PARTY_SCANDAL == "party_scandal"
        assert EventType.PARTY_SUCCESS == "party_success"
        assert EventType.POLICY_PROPOSAL == "policy_proposal"

        # IdeologicalBias
        assert IdeologicalBias.LEFT == "left"
        assert IdeologicalBias.CENTER_LEFT == "center_left"
        assert IdeologicalBias.CENTER == "center"
        assert IdeologicalBias.CENTER_RIGHT == "center_right"
        assert IdeologicalBias.RIGHT == "right"

    def test_models_are_pydantic_basemodels(self) -> None:
        """Verifica que los modelos son instancias de Pydantic BaseModel."""
        from pydantic import BaseModel

        from society_sim.domain import (
            CitizenSegment,
            Company,
            CompanySummary,
            DaySummary,
            Event,
            EventEffect,
            Party,
            PartySummary,
            Policy,
            PolicyEffect,
            WorldState,
        )

        # Verificar que todos son subclases de BaseModel
        assert issubclass(Company, BaseModel)
        assert issubclass(Party, BaseModel)
        assert issubclass(CitizenSegment, BaseModel)
        assert issubclass(Event, BaseModel)
        assert issubclass(EventEffect, BaseModel)
        assert issubclass(Policy, BaseModel)
        assert issubclass(PolicyEffect, BaseModel)
        assert issubclass(DaySummary, BaseModel)
        assert issubclass(PartySummary, BaseModel)
        assert issubclass(CompanySummary, BaseModel)
        assert issubclass(WorldState, BaseModel)

    def test_create_initial_world_is_callable(self) -> None:
        """Verifica que create_initial_world es una función callable."""
        from society_sim.domain import create_initial_world

        assert callable(create_initial_world)

    def test_create_initial_world_returns_world_state(self) -> None:
        """Verifica que create_initial_world retorna un WorldState válido."""
        from society_sim.domain import WorldState, create_initial_world

        world = create_initial_world()

        assert isinstance(world, WorldState)
        assert len(world.companies) >= 1
        assert len(world.parties) >= 1
        assert len(world.citizen_segments) >= 1

    def test_no_circular_imports(self) -> None:
        """
        Verifica que no hay imports circulares recargando el módulo.

        Si hubiera imports circulares, la recarga fallaría con ImportError.
        """
        import importlib

        import society_sim.domain

        # Recargar el módulo debería funcionar sin errores
        importlib.reload(society_sim.domain)

    def test_all_exports_in_dunder_all(self) -> None:
        """Verifica que __all__ contiene todos los exports esperados."""
        import society_sim.domain

        expected_exports = {
            "CitizenSegment",
            "Company",
            "CompanySummary",
            "DaySummary",
            "Event",
            "EventEffect",
            "EventType",
            "IdeologicalBias",
            "Party",
            "PartySummary",
            "Policy",
            "PolicyEffect",
            "Sector",
            "WorldState",
            "create_initial_world",
        }

        actual_exports = set(society_sim.domain.__all__)

        assert expected_exports == actual_exports, (
            f"Exports faltantes: {expected_exports - actual_exports}, "
            f"Exports extra: {actual_exports - expected_exports}"
        )

    def test_instantiation_with_imported_types(self) -> None:
        """
        Verifica que se pueden crear instancias usando los tipos importados.

        Este test asegura que los imports funcionan correctamente para uso real.
        """
        from society_sim.domain import (
            CitizenSegment,
            Company,
            CompanySummary,
            DaySummary,
            Event,
            EventEffect,
            EventType,
            IdeologicalBias,
            Party,
            PartySummary,
            Policy,
            PolicyEffect,
            Sector,
            WorldState,
        )

        # Crear instancias para verificar que los tipos funcionan
        company = Company(
            id="test-company",
            name="Test Company",
            sector=Sector.TECHNOLOGY,
            base_quality=0.5,
            base_price_level=0.5,
        )
        assert company.id == "test-company"

        party = Party(
            id="test-party",
            name="Test Party",
            ideology=IdeologicalBias.CENTER,
        )
        assert party.id == "test-party"

        segment = CitizenSegment(
            id="test-segment",
            name="Test Segment",
            size=1000,
            wealth_per_capita=10000.0,
            ideological_bias=IdeologicalBias.CENTER,
        )
        assert segment.id == "test-segment"

        effect = EventEffect(reputation_delta=5.0)
        event = Event(
            id="test-event",
            day=1,
            event_type=EventType.COMPANY_SUCCESS,
            narrative="Test narrative",
            effect=effect,
        )
        assert event.id == "test-event"

        policy_effect = PolicyEffect(target_sector=Sector.FOOD)
        policy = Policy(
            id="test-policy",
            name="Test Policy",
            description="Test description",
            proposed_by_party_id="test-party",
            effect=policy_effect,
            duration_days=10,
            remaining_days=10,
        )
        assert policy.id == "test-policy"

        party_summary = PartySummary(
            party_id="test-party",
            name="Test Party",
            popularity=50.0,
            reputation=50.0,
        )
        assert party_summary.party_id == "test-party"

        company_summary = CompanySummary(
            company_id="test-company",
            name="Test Company",
            stock_price=100.0,
            reputation=50.0,
            revenue=10000.0,
        )
        assert company_summary.company_id == "test-company"

        day_summary = DaySummary(
            day=1,
            total_revenue=50000.0,
            average_stock_price=100.0,
            average_satisfaction=50.0,
        )
        assert day_summary.day == 1

        world = WorldState(
            companies=[company],
            parties=[party],
            citizen_segments=[segment],
        )
        assert world.day == 0

