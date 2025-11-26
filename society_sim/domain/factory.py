"""
Funciones de inicialización del mundo para SocietySim.

Este módulo proporciona funciones factory para crear un WorldState inicial
con datos de ejemplo razonables para arrancar simulaciones.

Example:
    >>> from society_sim.domain import create_initial_world
    >>> world = create_initial_world()
    >>> len(world.companies)
    8
    >>> len(world.parties)
    4
    >>> len(world.citizen_segments)
    4
"""

from society_sim.domain.citizen_segment import CitizenSegment
from society_sim.domain.company import Company
from society_sim.domain.enums import IdeologicalBias, Sector
from society_sim.domain.party import Party
from society_sim.domain.world_state import WorldState


def _create_initial_companies() -> list[Company]:
    """
    Crea las empresas iniciales para la simulación.

    Genera 8 empresas distribuidas en los 6 sectores principales,
    con variedad de calidad y nivel de precios.

    Returns:
        Lista de empresas con datos de ejemplo balanceados.
    """
    return [
        # Sector HOUSING
        Company(
            id="housing-001",
            name="InmoHogar",
            sector=Sector.HOUSING,
            base_quality=0.7,
            base_price_level=0.6,
            reputation=55.0,
            stock_price=120.0,
            cash=2_000_000.0,
        ),
        # Sector FOOD
        Company(
            id="food-001",
            name="AlimentosFrescos",
            sector=Sector.FOOD,
            base_quality=0.8,
            base_price_level=0.4,
            reputation=60.0,
            stock_price=80.0,
            cash=1_500_000.0,
        ),
        Company(
            id="food-002",
            name="SuperEconómico",
            sector=Sector.FOOD,
            base_quality=0.5,
            base_price_level=0.2,
            reputation=45.0,
            stock_price=50.0,
            cash=800_000.0,
        ),
        # Sector TECHNOLOGY
        Company(
            id="tech-001",
            name="TechInnovadora",
            sector=Sector.TECHNOLOGY,
            base_quality=0.9,
            base_price_level=0.8,
            reputation=70.0,
            stock_price=200.0,
            cash=5_000_000.0,
        ),
        Company(
            id="tech-002",
            name="SoftwareSoluciones",
            sector=Sector.TECHNOLOGY,
            base_quality=0.7,
            base_price_level=0.5,
            reputation=50.0,
            stock_price=90.0,
            cash=1_200_000.0,
        ),
        # Sector CONSTRUCTION
        Company(
            id="const-001",
            name="ConstruyeMás",
            sector=Sector.CONSTRUCTION,
            base_quality=0.6,
            base_price_level=0.5,
            reputation=48.0,
            stock_price=75.0,
            cash=1_800_000.0,
        ),
        # Sector HEALTHCARE
        Company(
            id="health-001",
            name="SaludTotal",
            sector=Sector.HEALTHCARE,
            base_quality=0.85,
            base_price_level=0.7,
            reputation=65.0,
            stock_price=150.0,
            cash=3_000_000.0,
        ),
        # Sector FINANCE
        Company(
            id="finance-001",
            name="BancoSeguro",
            sector=Sector.FINANCE,
            base_quality=0.75,
            base_price_level=0.6,
            reputation=55.0,
            stock_price=180.0,
            cash=10_000_000.0,
        ),
    ]


def _create_initial_parties() -> list[Party]:
    """
    Crea los partidos políticos iniciales para la simulación.

    Genera 4 partidos con diferentes ideologías, uno de ellos
    marcado como partido en el gobierno.

    Returns:
        Lista de partidos políticos con datos de ejemplo.
    """
    return [
        Party(
            id="party-left",
            name="Partido Progresista",
            ideology=IdeologicalBias.LEFT,
            popularity=22.0,
            reputation=52.0,
            in_government=False,
        ),
        Party(
            id="party-center-left",
            name="Partido Socialdemócrata",
            ideology=IdeologicalBias.CENTER_LEFT,
            popularity=28.0,
            reputation=55.0,
            in_government=True,  # Partido en el gobierno
        ),
        Party(
            id="party-center-right",
            name="Partido Liberal",
            ideology=IdeologicalBias.CENTER_RIGHT,
            popularity=25.0,
            reputation=50.0,
            in_government=False,
        ),
        Party(
            id="party-right",
            name="Partido Conservador",
            ideology=IdeologicalBias.RIGHT,
            popularity=20.0,
            reputation=48.0,
            in_government=False,
        ),
    ]


def _create_initial_citizen_segments() -> list[CitizenSegment]:
    """
    Crea los segmentos ciudadanos iniciales para la simulación.

    Genera 4 segmentos representando diferentes clases socioeconómicas:
    - Clase Alta: pequeño tamaño, alta riqueza
    - Clase Media: tamaño medio, riqueza media
    - Clase Trabajadora: tamaño grande, baja riqueza
    - Desempleados/Precarios: tamaño pequeño, muy baja riqueza

    Returns:
        Lista de segmentos ciudadanos con datos de ejemplo.
    """
    return [
        CitizenSegment(
            id="seg-upper",
            name="Clase Alta",
            size=500_000,  # 5% de población
            wealth_per_capita=200_000.0,
            satisfaction=70.0,
            ideological_bias=IdeologicalBias.CENTER_RIGHT,
            preferred_party_id="party-center-right",
            consumption_rate=0.15,  # Mayor propensión al consumo
        ),
        CitizenSegment(
            id="seg-middle",
            name="Clase Media",
            size=3_000_000,  # 30% de población
            wealth_per_capita=50_000.0,
            satisfaction=55.0,
            ideological_bias=IdeologicalBias.CENTER,
            preferred_party_id="party-center-left",
            consumption_rate=0.10,
        ),
        CitizenSegment(
            id="seg-working",
            name="Clase Trabajadora",
            size=5_000_000,  # 50% de población
            wealth_per_capita=20_000.0,
            satisfaction=45.0,
            ideological_bias=IdeologicalBias.CENTER_LEFT,
            preferred_party_id="party-center-left",
            consumption_rate=0.08,
        ),
        CitizenSegment(
            id="seg-precarious",
            name="Desempleados y Precarios",
            size=1_500_000,  # 15% de población
            wealth_per_capita=5_000.0,
            satisfaction=30.0,
            ideological_bias=IdeologicalBias.LEFT,
            preferred_party_id="party-left",
            consumption_rate=0.05,  # Menor propensión al consumo (ahorran más por necesidad)
        ),
    ]


def create_initial_world() -> WorldState:
    """
    Crea un WorldState inicial con datos de ejemplo razonables.

    Esta función genera un estado del mundo completo y coherente para
    arrancar simulaciones, incluyendo:
    - 8 empresas distribuidas en los 6 sectores principales
    - 4 partidos políticos con diferentes ideologías (uno en gobierno)
    - 4 segmentos ciudadanos representando diferentes clases sociales

    Los datos están balanceados para permitir dinámicas de mercado
    y políticas interesantes desde el inicio.

    Returns:
        WorldState configurado con entidades iniciales.

    Example:
        >>> world = create_initial_world()
        >>> world.day
        0
        >>> len(world.companies)
        8
        >>> any(p.in_government for p in world.parties)
        True
        >>> sum(s.size for s in world.citizen_segments)
        10000000
    """
    return WorldState(
        day=0,
        companies=_create_initial_companies(),
        parties=_create_initial_parties(),
        citizen_segments=_create_initial_citizen_segments(),
        active_policies=[],
        events_today=[],
        history=[],
    )

