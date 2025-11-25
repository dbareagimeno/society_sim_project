"""
Tests unitarios para el modelo Policy y PolicyEffect.

Verifica la creación, validación, serialización y comportamiento
del tick de políticas gubernamentales en la simulación.
"""

import json

import pytest
from pydantic import ValidationError

from society_sim.domain import Policy, PolicyEffect, Sector


class TestPolicyEffect:
    """Tests para la clase PolicyEffect."""

    def test_create_policy_effect_with_defaults(self):
        """PolicyEffect se puede crear con todos los valores por defecto."""
        effect = PolicyEffect()

        assert effect.target_sector is None
        assert effect.price_modifier == 1.0
        assert effect.tax_rate_delta == 0.0
        assert effect.subsidy_amount == 0.0
        assert effect.reputation_boost == 0.0

    def test_create_policy_effect_with_custom_values(self):
        """PolicyEffect acepta valores personalizados."""
        effect = PolicyEffect(
            target_sector=Sector.HOUSING,
            price_modifier=0.85,
            tax_rate_delta=0.05,
            subsidy_amount=100_000.0,
            reputation_boost=5.0,
        )

        assert effect.target_sector == Sector.HOUSING
        assert effect.price_modifier == 0.85
        assert effect.tax_rate_delta == 0.05
        assert effect.subsidy_amount == 100_000.0
        assert effect.reputation_boost == 5.0

    def test_policy_effect_target_sector_accepts_all_sectors(self):
        """PolicyEffect acepta cualquier sector como target."""
        for sector in Sector:
            effect = PolicyEffect(target_sector=sector)
            assert effect.target_sector == sector

    def test_policy_effect_price_modifier_must_be_positive(self):
        """price_modifier debe ser mayor que 0."""
        with pytest.raises(ValidationError) as exc_info:
            PolicyEffect(price_modifier=0.0)
        assert "price_modifier" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            PolicyEffect(price_modifier=-0.5)
        assert "price_modifier" in str(exc_info.value)

    def test_policy_effect_subsidy_amount_must_be_non_negative(self):
        """subsidy_amount no puede ser negativo."""
        with pytest.raises(ValidationError) as exc_info:
            PolicyEffect(subsidy_amount=-1000.0)
        assert "subsidy_amount" in str(exc_info.value)

    def test_policy_effect_allows_negative_tax_rate_delta(self):
        """tax_rate_delta puede ser negativo (reducción de impuestos)."""
        effect = PolicyEffect(tax_rate_delta=-0.10)
        assert effect.tax_rate_delta == -0.10

    def test_policy_effect_allows_negative_reputation_boost(self):
        """reputation_boost puede ser negativo (penalización)."""
        effect = PolicyEffect(reputation_boost=-5.0)
        assert effect.reputation_boost == -5.0

    def test_policy_effect_is_immutable(self):
        """PolicyEffect es inmutable una vez creado."""
        effect = PolicyEffect(price_modifier=0.9)

        with pytest.raises(ValidationError):
            effect.price_modifier = 1.1

    def test_policy_effect_serializes_to_json(self):
        """PolicyEffect se puede serializar a JSON."""
        effect = PolicyEffect(
            target_sector=Sector.TECHNOLOGY,
            price_modifier=1.2,
            tax_rate_delta=0.03,
            subsidy_amount=50_000.0,
            reputation_boost=3.0,
        )

        json_str = effect.model_dump_json()
        data = json.loads(json_str)

        assert data["target_sector"] == "technology"
        assert data["price_modifier"] == 1.2
        assert data["tax_rate_delta"] == 0.03
        assert data["subsidy_amount"] == 50_000.0
        assert data["reputation_boost"] == 3.0

    def test_policy_effect_deserializes_from_json(self):
        """PolicyEffect se puede deserializar desde JSON."""
        json_str = """{
            "target_sector": "healthcare",
            "price_modifier": 0.8,
            "tax_rate_delta": -0.02,
            "subsidy_amount": 25000.0,
            "reputation_boost": 2.0
        }"""

        effect = PolicyEffect.model_validate_json(json_str)

        assert effect.target_sector == Sector.HEALTHCARE
        assert effect.price_modifier == 0.8
        assert effect.tax_rate_delta == -0.02
        assert effect.subsidy_amount == 25_000.0
        assert effect.reputation_boost == 2.0

    def test_policy_effect_with_null_target_sector(self):
        """PolicyEffect acepta target_sector como None."""
        json_str = '{"target_sector": null, "price_modifier": 1.0}'
        effect = PolicyEffect.model_validate_json(json_str)
        assert effect.target_sector is None


class TestPolicy:
    """Tests para la clase Policy."""

    @pytest.fixture
    def sample_effect(self) -> PolicyEffect:
        """Fixture que proporciona un PolicyEffect de ejemplo."""
        return PolicyEffect(
            target_sector=Sector.HOUSING,
            price_modifier=0.9,
            subsidy_amount=50_000.0,
        )

    def test_create_policy_with_required_fields(self, sample_effect: PolicyEffect):
        """Se puede crear una política con campos requeridos."""
        policy = Policy(
            id="pol-001",
            name="Ley de Vivienda",
            description="Control de precios y subsidios para vivienda",
            proposed_by_party_id="party-001",
            effect=sample_effect,
            duration_days=30,
            remaining_days=30,
        )

        assert policy.id == "pol-001"
        assert policy.name == "Ley de Vivienda"
        assert policy.description == "Control de precios y subsidios para vivienda"
        assert policy.proposed_by_party_id == "party-001"
        assert policy.effect == sample_effect
        assert policy.duration_days == 30
        assert policy.remaining_days == 30
        assert policy.is_active is True

    def test_create_policy_with_is_active_false(self, sample_effect: PolicyEffect):
        """Se puede crear una política inactiva."""
        policy = Policy(
            id="pol-002",
            name="Ley Expirada",
            description="Una política que ya no está vigente",
            proposed_by_party_id="party-001",
            effect=sample_effect,
            duration_days=10,
            remaining_days=0,
            is_active=False,
        )

        assert policy.is_active is False
        assert policy.remaining_days == 0

    def test_policy_requires_id(self, sample_effect: PolicyEffect):
        """Policy requiere un id."""
        with pytest.raises(ValidationError) as exc_info:
            Policy(
                name="Test",
                description="Test",
                proposed_by_party_id="party-001",
                effect=sample_effect,
                duration_days=10,
                remaining_days=10,
            )
        assert "id" in str(exc_info.value)

    def test_policy_requires_name(self, sample_effect: PolicyEffect):
        """Policy requiere un nombre."""
        with pytest.raises(ValidationError) as exc_info:
            Policy(
                id="pol-001",
                description="Test",
                proposed_by_party_id="party-001",
                effect=sample_effect,
                duration_days=10,
                remaining_days=10,
            )
        assert "name" in str(exc_info.value)

    def test_policy_requires_description(self, sample_effect: PolicyEffect):
        """Policy requiere una descripción."""
        with pytest.raises(ValidationError) as exc_info:
            Policy(
                id="pol-001",
                name="Test",
                proposed_by_party_id="party-001",
                effect=sample_effect,
                duration_days=10,
                remaining_days=10,
            )
        assert "description" in str(exc_info.value)

    def test_policy_requires_proposed_by_party_id(self, sample_effect: PolicyEffect):
        """Policy requiere un proposed_by_party_id."""
        with pytest.raises(ValidationError) as exc_info:
            Policy(
                id="pol-001",
                name="Test",
                description="Test",
                effect=sample_effect,
                duration_days=10,
                remaining_days=10,
            )
        assert "proposed_by_party_id" in str(exc_info.value)

    def test_policy_requires_effect(self):
        """Policy requiere un efecto."""
        with pytest.raises(ValidationError) as exc_info:
            Policy(
                id="pol-001",
                name="Test",
                description="Test",
                proposed_by_party_id="party-001",
                duration_days=10,
                remaining_days=10,
            )
        assert "effect" in str(exc_info.value)

    def test_policy_duration_days_must_be_positive(self, sample_effect: PolicyEffect):
        """duration_days debe ser mayor que 0."""
        with pytest.raises(ValidationError) as exc_info:
            Policy(
                id="pol-001",
                name="Test",
                description="Test",
                proposed_by_party_id="party-001",
                effect=sample_effect,
                duration_days=0,
                remaining_days=0,
            )
        assert "duration_days" in str(exc_info.value)

    def test_policy_remaining_days_cannot_be_negative(
        self, sample_effect: PolicyEffect
    ):
        """remaining_days no puede ser negativo."""
        with pytest.raises(ValidationError) as exc_info:
            Policy(
                id="pol-001",
                name="Test",
                description="Test",
                proposed_by_party_id="party-001",
                effect=sample_effect,
                duration_days=10,
                remaining_days=-1,
            )
        assert "remaining_days" in str(exc_info.value)

    def test_policy_remaining_days_cannot_exceed_duration(
        self, sample_effect: PolicyEffect
    ):
        """remaining_days no puede ser mayor que duration_days."""
        with pytest.raises(ValidationError) as exc_info:
            Policy(
                id="pol-001",
                name="Test",
                description="Test",
                proposed_by_party_id="party-001",
                effect=sample_effect,
                duration_days=10,
                remaining_days=15,
            )
        assert "remaining_days" in str(exc_info.value)


class TestPolicyTick:
    """Tests para el método tick() de Policy."""

    @pytest.fixture
    def sample_effect(self) -> PolicyEffect:
        """Fixture que proporciona un PolicyEffect de ejemplo."""
        return PolicyEffect(target_sector=Sector.TECHNOLOGY)

    def test_tick_decrements_remaining_days(self, sample_effect: PolicyEffect):
        """tick() decrementa remaining_days en 1."""
        policy = Policy(
            id="pol-001",
            name="Test",
            description="Test policy",
            proposed_by_party_id="party-001",
            effect=sample_effect,
            duration_days=10,
            remaining_days=5,
        )

        updated = policy.tick()

        assert updated.remaining_days == 4
        assert updated.is_active is True

    def test_tick_returns_new_instance(self, sample_effect: PolicyEffect):
        """tick() retorna una nueva instancia, no modifica la original."""
        policy = Policy(
            id="pol-001",
            name="Test",
            description="Test policy",
            proposed_by_party_id="party-001",
            effect=sample_effect,
            duration_days=10,
            remaining_days=5,
        )

        updated = policy.tick()

        # Original no cambia
        assert policy.remaining_days == 5
        assert policy.is_active is True

        # Nueva instancia tiene los valores actualizados
        assert updated.remaining_days == 4
        assert updated is not policy

    def test_tick_deactivates_when_remaining_reaches_zero(
        self, sample_effect: PolicyEffect
    ):
        """tick() desactiva la política cuando remaining_days llega a 0."""
        policy = Policy(
            id="pol-001",
            name="Test",
            description="Test policy",
            proposed_by_party_id="party-001",
            effect=sample_effect,
            duration_days=10,
            remaining_days=1,
        )

        updated = policy.tick()

        assert updated.remaining_days == 0
        assert updated.is_active is False

    def test_tick_on_already_expired_policy(self, sample_effect: PolicyEffect):
        """tick() en política expirada mantiene remaining_days en 0."""
        policy = Policy(
            id="pol-001",
            name="Test",
            description="Test policy",
            proposed_by_party_id="party-001",
            effect=sample_effect,
            duration_days=10,
            remaining_days=0,
            is_active=False,
        )

        updated = policy.tick()

        assert updated.remaining_days == 0
        assert updated.is_active is False

    def test_tick_multiple_times_until_expiry(self, sample_effect: PolicyEffect):
        """tick() múltiples veces hasta expirar funciona correctamente."""
        policy = Policy(
            id="pol-001",
            name="Test",
            description="Test policy",
            proposed_by_party_id="party-001",
            effect=sample_effect,
            duration_days=3,
            remaining_days=3,
        )

        # Día 1: remaining = 2
        policy = policy.tick()
        assert policy.remaining_days == 2
        assert policy.is_active is True

        # Día 2: remaining = 1
        policy = policy.tick()
        assert policy.remaining_days == 1
        assert policy.is_active is True

        # Día 3: remaining = 0, se desactiva
        policy = policy.tick()
        assert policy.remaining_days == 0
        assert policy.is_active is False

        # Día 4+: permanece en 0 e inactivo
        policy = policy.tick()
        assert policy.remaining_days == 0
        assert policy.is_active is False

    def test_tick_preserves_other_fields(self, sample_effect: PolicyEffect):
        """tick() preserva todos los demás campos de la política."""
        policy = Policy(
            id="pol-001",
            name="Ley Test",
            description="Una política de prueba",
            proposed_by_party_id="party-001",
            effect=sample_effect,
            duration_days=10,
            remaining_days=5,
        )

        updated = policy.tick()

        assert updated.id == policy.id
        assert updated.name == policy.name
        assert updated.description == policy.description
        assert updated.proposed_by_party_id == policy.proposed_by_party_id
        assert updated.effect == policy.effect
        assert updated.duration_days == policy.duration_days


class TestPolicySerialization:
    """Tests de serialización y deserialización JSON."""

    @pytest.fixture
    def sample_effect(self) -> PolicyEffect:
        """Fixture que proporciona un PolicyEffect de ejemplo."""
        return PolicyEffect(
            target_sector=Sector.FINANCE,
            price_modifier=1.1,
            tax_rate_delta=0.02,
            subsidy_amount=0.0,
            reputation_boost=-2.0,
        )

    def test_serialize_policy_to_json(self, sample_effect: PolicyEffect):
        """Policy se puede serializar a JSON."""
        policy = Policy(
            id="pol-001",
            name="Regulación Financiera",
            description="Aumenta impuestos y precios en el sector financiero",
            proposed_by_party_id="party-002",
            effect=sample_effect,
            duration_days=60,
            remaining_days=45,
            is_active=True,
        )

        json_str = policy.model_dump_json()
        data = json.loads(json_str)

        assert data["id"] == "pol-001"
        assert data["name"] == "Regulación Financiera"
        assert data["proposed_by_party_id"] == "party-002"
        assert data["duration_days"] == 60
        assert data["remaining_days"] == 45
        assert data["is_active"] is True
        assert data["effect"]["target_sector"] == "finance"
        assert data["effect"]["price_modifier"] == 1.1

    def test_deserialize_policy_from_json(self):
        """Policy se puede deserializar desde JSON."""
        json_str = """
        {
            "id": "pol-002",
            "name": "Subsidio Sanitario",
            "description": "Subsidios para el sector salud",
            "proposed_by_party_id": "party-001",
            "effect": {
                "target_sector": "healthcare",
                "price_modifier": 0.8,
                "tax_rate_delta": -0.01,
                "subsidy_amount": 100000.0,
                "reputation_boost": 5.0
            },
            "duration_days": 90,
            "remaining_days": 90,
            "is_active": true
        }
        """

        policy = Policy.model_validate_json(json_str)

        assert policy.id == "pol-002"
        assert policy.name == "Subsidio Sanitario"
        assert policy.proposed_by_party_id == "party-001"
        assert policy.effect.target_sector == Sector.HEALTHCARE
        assert policy.effect.price_modifier == 0.8
        assert policy.effect.subsidy_amount == 100_000.0
        assert policy.duration_days == 90
        assert policy.is_active is True

    def test_roundtrip_serialization(self, sample_effect: PolicyEffect):
        """Policy mantiene los datos tras serializar y deserializar."""
        original = Policy(
            id="pol-003",
            name="Test Policy",
            description="A test policy for serialization",
            proposed_by_party_id="party-003",
            effect=sample_effect,
            duration_days=30,
            remaining_days=15,
            is_active=True,
        )

        # Serializar y deserializar
        json_str = original.model_dump_json()
        restored = Policy.model_validate_json(json_str)

        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.description == original.description
        assert restored.proposed_by_party_id == original.proposed_by_party_id
        assert restored.effect.target_sector == original.effect.target_sector
        assert restored.effect.price_modifier == original.effect.price_modifier
        assert restored.duration_days == original.duration_days
        assert restored.remaining_days == original.remaining_days
        assert restored.is_active == original.is_active


class TestPolicyEdgeCases:
    """Tests de casos límite."""

    def test_policy_with_minimal_duration(self):
        """Policy puede tener duración mínima de 1 día."""
        effect = PolicyEffect()
        policy = Policy(
            id="pol-001",
            name="Flash Policy",
            description="Very short policy",
            proposed_by_party_id="party-001",
            effect=effect,
            duration_days=1,
            remaining_days=1,
        )

        assert policy.duration_days == 1
        assert policy.remaining_days == 1

        # Después de tick, expira
        updated = policy.tick()
        assert updated.remaining_days == 0
        assert updated.is_active is False

    def test_policy_with_no_sector_target(self):
        """Policy puede no tener sector objetivo (afecta a todos)."""
        effect = PolicyEffect(
            target_sector=None,
            tax_rate_delta=0.05,
        )
        policy = Policy(
            id="pol-001",
            name="Impuesto General",
            description="Impuesto que afecta a todos los sectores",
            proposed_by_party_id="party-001",
            effect=effect,
            duration_days=365,
            remaining_days=365,
        )

        assert policy.effect.target_sector is None

    def test_policy_boundary_price_modifier(self):
        """PolicyEffect acepta price_modifier cercano a 0."""
        effect = PolicyEffect(price_modifier=0.01)
        assert effect.price_modifier == 0.01

    def test_policy_large_values(self):
        """Policy acepta valores grandes."""
        effect = PolicyEffect(
            subsidy_amount=1_000_000_000.0,
        )
        policy = Policy(
            id="pol-001",
            name="Mega Subsidio",
            description="Subsidio masivo",
            proposed_by_party_id="party-001",
            effect=effect,
            duration_days=3650,  # 10 años
            remaining_days=3650,
        )

        assert policy.duration_days == 3650
        assert policy.effect.subsidy_amount == 1_000_000_000.0

