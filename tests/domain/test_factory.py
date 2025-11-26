"""
Tests para la función de inicialización del mundo.

Este módulo verifica que create_initial_world() genera un WorldState
válido con datos coherentes y balanceados.
"""

from society_sim.domain import (
    CitizenSegment,
    Company,
    IdeologicalBias,
    Party,
    Sector,
    WorldState,
    create_initial_world,
)


class TestCreateInitialWorld:
    """Tests para la función create_initial_world."""

    def test_returns_valid_world_state(self) -> None:
        """Verifica que la función retorna un WorldState válido."""
        world = create_initial_world()

        assert isinstance(world, WorldState)
        assert world.day == 0

    def test_has_required_companies(self) -> None:
        """Verifica que se crean entre 6 y 10 empresas."""
        world = create_initial_world()

        assert 6 <= len(world.companies) <= 10

    def test_companies_cover_all_sectors(self) -> None:
        """Verifica que hay al menos una empresa por sector principal."""
        world = create_initial_world()
        sectors_covered = {company.sector for company in world.companies}

        # Todos los sectores deben estar cubiertos
        for sector in Sector:
            assert sector in sectors_covered, f"Falta empresa en sector {sector}"

    def test_companies_have_variety_in_quality_and_price(self) -> None:
        """Verifica que hay variedad en calidad y precio de empresas."""
        world = create_initial_world()

        qualities = [c.base_quality for c in world.companies]
        prices = [c.base_price_level for c in world.companies]

        # Verificar que hay variedad (rango > 0.2)
        assert max(qualities) - min(qualities) >= 0.2
        assert max(prices) - min(prices) >= 0.2

    def test_companies_are_valid(self) -> None:
        """Verifica que todas las empresas tienen datos válidos."""
        world = create_initial_world()

        for company in world.companies:
            assert isinstance(company, Company)
            assert company.id
            assert company.name
            assert 0.0 <= company.base_quality <= 1.0
            assert 0.0 <= company.base_price_level <= 1.0
            assert 0.0 <= company.reputation <= 100.0
            assert company.stock_price > 0
            assert company.cash >= 0

    def test_has_required_parties(self) -> None:
        """Verifica que se crean entre 3 y 4 partidos."""
        world = create_initial_world()

        assert 3 <= len(world.parties) <= 4

    def test_parties_have_different_ideologies(self) -> None:
        """Verifica que los partidos tienen ideologías diferentes."""
        world = create_initial_world()
        ideologies = [party.ideology for party in world.parties]

        # Al menos 3 ideologías diferentes
        assert len(set(ideologies)) >= 3

    def test_one_party_in_government(self) -> None:
        """Verifica que exactamente un partido está en el gobierno."""
        world = create_initial_world()
        parties_in_government = [p for p in world.parties if p.in_government]

        assert len(parties_in_government) == 1

    def test_parties_are_valid(self) -> None:
        """Verifica que todos los partidos tienen datos válidos."""
        world = create_initial_world()

        for party in world.parties:
            assert isinstance(party, Party)
            assert party.id
            assert party.name
            assert isinstance(party.ideology, IdeologicalBias)
            assert 0.0 <= party.popularity <= 100.0
            assert 0.0 <= party.reputation <= 100.0

    def test_has_required_citizen_segments(self) -> None:
        """Verifica que se crean entre 3 y 4 segmentos ciudadanos."""
        world = create_initial_world()

        assert 3 <= len(world.citizen_segments) <= 4

    def test_citizen_segments_have_diverse_wealth(self) -> None:
        """Verifica que hay diversidad en riqueza de segmentos."""
        world = create_initial_world()
        wealth_levels = [s.wealth_per_capita for s in world.citizen_segments]

        # Debe haber al menos 3x diferencia entre el más rico y el más pobre
        assert max(wealth_levels) / min(wealth_levels) >= 3

    def test_citizen_segments_have_diverse_sizes(self) -> None:
        """Verifica que hay diversidad en tamaño de segmentos."""
        world = create_initial_world()
        sizes = [s.size for s in world.citizen_segments]

        # Debe haber diferencia significativa en tamaños
        assert max(sizes) / min(sizes) >= 2

    def test_citizen_segments_are_valid(self) -> None:
        """Verifica que todos los segmentos tienen datos válidos."""
        world = create_initial_world()

        for segment in world.citizen_segments:
            assert isinstance(segment, CitizenSegment)
            assert segment.id
            assert segment.name
            assert segment.size > 0
            assert segment.wealth_per_capita >= 0
            assert 0.0 <= segment.satisfaction <= 100.0
            assert 0.0 <= segment.consumption_rate <= 1.0
            assert isinstance(segment.ideological_bias, IdeologicalBias)

    def test_total_population_is_reasonable(self) -> None:
        """Verifica que la población total es razonable."""
        world = create_initial_world()
        total_population = sum(s.size for s in world.citizen_segments)

        # Población entre 1 millón y 100 millones
        assert 1_000_000 <= total_population <= 100_000_000

    def test_world_state_has_empty_initial_state(self) -> None:
        """Verifica que el estado inicial no tiene eventos ni políticas activas."""
        world = create_initial_world()

        assert world.events_today == []
        assert world.active_policies == []
        assert world.history == []

    def test_preferred_party_ids_reference_existing_parties(self) -> None:
        """Verifica que los party_id preferidos existen en la lista de partidos."""
        world = create_initial_world()
        party_ids = {party.id for party in world.parties}

        for segment in world.citizen_segments:
            if segment.preferred_party_id is not None:
                assert segment.preferred_party_id in party_ids, (
                    f"Segmento {segment.name} referencia partido inexistente: "
                    f"{segment.preferred_party_id}"
                )

    def test_world_is_json_serializable(self) -> None:
        """Verifica que el WorldState inicial se puede serializar a JSON."""
        world = create_initial_world()

        # model_dump_json debería funcionar sin errores
        json_str = world.model_dump_json()
        assert isinstance(json_str, str)
        assert len(json_str) > 0

    def test_world_can_be_recreated_from_json(self) -> None:
        """Verifica que el WorldState se puede recrear desde JSON."""
        world = create_initial_world()
        json_str = world.model_dump_json()

        recreated_world = WorldState.model_validate_json(json_str)

        assert recreated_world.day == world.day
        assert len(recreated_world.companies) == len(world.companies)
        assert len(recreated_world.parties) == len(world.parties)
        assert len(recreated_world.citizen_segments) == len(world.citizen_segments)


class TestInitialWorldCoherence:
    """Tests de coherencia de datos del mundo inicial."""

    def test_satisfaction_follows_wealth_pattern(self) -> None:
        """
        Verifica que la satisfacción sigue un patrón coherente con la riqueza.
        
        Los segmentos más ricos deberían tener mayor satisfacción inicial.
        """
        world = create_initial_world()

        # Ordenar por riqueza
        sorted_by_wealth = sorted(
            world.citizen_segments,
            key=lambda s: s.wealth_per_capita,
            reverse=True,
        )

        # El más rico debería tener mayor satisfacción que el más pobre
        richest = sorted_by_wealth[0]
        poorest = sorted_by_wealth[-1]

        assert richest.satisfaction > poorest.satisfaction

    def test_high_quality_companies_have_higher_prices(self) -> None:
        """
        Verifica coherencia entre calidad y precio.
        
        En promedio, empresas de mayor calidad deberían tener precios más altos.
        """
        world = create_initial_world()

        high_quality = [c for c in world.companies if c.base_quality >= 0.7]
        low_quality = [c for c in world.companies if c.base_quality < 0.7]

        if high_quality and low_quality:
            avg_price_high = sum(c.base_price_level for c in high_quality) / len(
                high_quality
            )
            avg_price_low = sum(c.base_price_level for c in low_quality) / len(
                low_quality
            )

            # Las empresas de alta calidad deberían tender a ser más caras
            assert avg_price_high >= avg_price_low

    def test_parties_popularity_sums_near_100(self) -> None:
        """
        Verifica que la suma de popularidades es cercana a 100.
        
        Esto representa que la popularidad es aproximadamente un share del electorado.
        """
        world = create_initial_world()
        total_popularity = sum(p.popularity for p in world.parties)

        # La suma debería estar entre 80 y 120 (permitimos algo de flexibilidad)
        assert 80 <= total_popularity <= 120

    def test_segment_ideologies_are_diverse(self) -> None:
        """Verifica que los segmentos tienen ideologías diversas."""
        world = create_initial_world()
        ideologies = {s.ideological_bias for s in world.citizen_segments}

        # Al menos 3 ideologías diferentes entre los segmentos
        assert len(ideologies) >= 3

