"""
pytest test suite for class_attributes exercises.
Run with:  pytest test_exercises.py -v
"""

import pytest
from exercises import Circle, User, ServerConfig, BrokenTeam, FixedTeam, Plugin



# Exercise 1 - Circle (shared constant PI)

class TestCircle:
    def test_pi_is_class_attribute(self):
        assert hasattr(Circle, "PI"), "Circle must have a class attribute PI"
        assert Circle.PI == 3.14159

    def test_pi_shared_across_instances(self):
        c1 = Circle(1)
        c2 = Circle(5)
        assert c1.PI is Circle.PI is c2.PI

    def test_radius_is_instance_attribute(self):
        c = Circle(7)
        assert c.radius == 7

    def test_area(self):
        c = Circle(2)
        assert c.area() == pytest.approx(3.14159 * 4, rel=1e-5)

    def test_circumference(self):
        c = Circle(3)
        assert c.circumference() == pytest.approx(2 * 3.14159 * 3, rel=1e-5)

    def test_different_radii(self):
        assert Circle(1).area() != Circle(2).area()


# ============================================================
# Exercise 2 — User (instance counter)
# ============================================================

class TestUser:
    def setup_method(self):
        """Reset counter before every test so they don't bleed into each other."""
        User.reset()

    def test_count_starts_at_zero(self):
        assert User.count == 0

    def test_count_increments_on_creation(self):
        User("alice")
        assert User.count == 1

    def test_count_increments_multiple(self):
        User("alice")
        User("bob")
        User("carol")
        assert User.count == 3

    def test_count_is_class_attribute(self):
        User("alice")
        # All instances must see the same count
        u1 = User("bob")
        u2 = User("carol")
        assert u1.count == u2.count == User.count == 3

    def test_reset_sets_count_to_zero(self):
        User("alice")
        User("bob")
        User.reset()
        assert User.count == 0

    def test_username_stored(self):
        u = User("dave")
        assert u.username == "dave"


# ============================================================
# Exercise 3 — ServerConfig (default class attributes)
# ============================================================

class TestServerConfig:
    def test_class_defaults_exist(self):
        assert ServerConfig.host == "localhost"
        assert ServerConfig.port == 8080
        assert ServerConfig.timeout == 30

    def test_instance_inherits_defaults(self):
        cfg = ServerConfig()
        assert cfg.host == "localhost"
        assert cfg.port == 8080
        assert cfg.timeout == 30

    def test_instance_override_does_not_change_class(self):
        cfg = ServerConfig()
        cfg.port = 9090
        assert cfg.port == 9090
        assert ServerConfig.port == 8080   # class attribute unchanged

    def test_two_instances_independent(self):
        cfg1 = ServerConfig()
        cfg2 = ServerConfig()
        cfg1.timeout = 60
        assert cfg2.timeout == 30          # cfg2 still uses class default

    def test_class_attribute_change_propagates(self):
        """Changing the class attribute affects instances that haven't overridden it."""
        original = ServerConfig.host
        try:
            ServerConfig.host = "example.com"
            cfg = ServerConfig()
            assert cfg.host == "example.com"
        finally:
            ServerConfig.host = original   # restore


# ============================================================
# Exercise 4 — Mutable trap (BrokenTeam vs FixedTeam)
# ============================================================

class TestBrokenTeam:
    def test_broken_shares_list(self):
        """Demonstrate the bug: two teams bleed into each other."""
        # Reset the shared list before test
        BrokenTeam.members = []

        t1 = BrokenTeam("Alpha")
        t2 = BrokenTeam("Beta")

        t1.add_member("Alice")
        # Because members is a class attribute, t2 sees Alice too
        assert "Alice" in t2.members, (
            "BrokenTeam should share the members list (this is the bug)"
        )


class TestFixedTeam:
    def test_each_instance_has_own_list(self):
        t1 = FixedTeam("Alpha")
        t2 = FixedTeam("Beta")

        t1.add_member("Alice")
        assert "Alice" in t1.members
        assert "Alice" not in t2.members   # t2 must be unaffected

    def test_add_multiple_members(self):
        t = FixedTeam("Gamma")
        t.add_member("Bob")
        t.add_member("Carol")
        assert t.members == ["Bob", "Carol"]

    def test_empty_on_creation(self):
        t = FixedTeam("Delta")
        assert t.members == []

    def test_name_stored(self):
        t = FixedTeam("Epsilon")
        assert t.name == "Epsilon"


# ============================================================
# Exercise 5 — Plugin registry
# ============================================================

class TestPlugin:
    def setup_method(self):
        Plugin.reset()

    def test_registry_is_class_attribute(self):
        assert hasattr(Plugin, "registry")
        assert isinstance(Plugin.registry, dict)

    def test_plugin_registers_on_creation(self):
        p = Plugin("auth")
        assert "auth" in Plugin.registry
        assert Plugin.registry["auth"] is p

    def test_multiple_plugins(self):
        Plugin("auth")
        Plugin("cache")
        Plugin("logger")
        assert set(Plugin.registry.keys()) == {"auth", "cache", "logger"}

    def test_get_returns_plugin(self):
        p = Plugin("auth")
        assert Plugin.get("auth") is p

    def test_get_returns_none_for_missing(self):
        assert Plugin.get("nonexistent") is None

    def test_reset_clears_registry(self):
        Plugin("auth")
        Plugin.reset()
        assert Plugin.registry == {}

    def test_name_stored_on_instance(self):
        p = Plugin("my_plugin")
        assert p.name == "my_plugin"
