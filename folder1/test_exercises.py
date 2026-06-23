import pytest

from exercises import (
    # Exercise 1
    BelowAbsoluteZeroError,
    InvalidScaleError,
    TemperatureError,
    convert_temperature,
    # Exercise 2
    UserAlreadyExistsError,
    UserNotFoundError,
    UserRegistry,
    UserRegistryError,
    # Exercise 3
    ParseError,
    PipelineError,
    ProcessError,
    parse_record,
    process_record,
    run_pipeline,
)


# EXERCISE 1 — Temperature Converter


class TestTemperatureExceptionHierarchy:
    """BelowAbsoluteZeroError and InvalidScaleError must be TemperatureErrors."""

    def test_below_absolute_zero_is_temperature_error(self):
        assert issubclass(BelowAbsoluteZeroError, TemperatureError)

    def test_invalid_scale_is_temperature_error(self):
        assert issubclass(InvalidScaleError, TemperatureError)

    def test_temperature_error_is_exception(self):
        assert issubclass(TemperatureError, Exception)


class TestBelowAbsoluteZeroError:

    def test_raises_correctly(self):
        with pytest.raises(BelowAbsoluteZeroError):
            raise BelowAbsoluteZeroError(-300.0)

    def test_stores_value_celsius(self):
        exc = BelowAbsoluteZeroError(-300.0)
        assert exc.value_celsius == -300.0

    def test_message_contains_value(self):
        exc = BelowAbsoluteZeroError(-300.0)
        assert "-300" in str(exc)

    def test_message_contains_absolute_zero(self):
        exc = BelowAbsoluteZeroError(-300.0)
        assert "-273.15" in str(exc)

    def test_catchable_as_temperature_error(self):
        with pytest.raises(TemperatureError):
            raise BelowAbsoluteZeroError(-300.0)


class TestInvalidScaleError:

    def test_raises_correctly(self):
        with pytest.raises(InvalidScaleError):
            raise InvalidScaleError("X")

    def test_stores_scale(self):
        exc = InvalidScaleError("Z")
        assert exc.scale == "Z"

    def test_stores_valid_scales(self):
        exc = InvalidScaleError("Z")
        assert set(exc.valid_scales) == {"C", "F", "K"}

    def test_message_contains_bad_scale(self):
        exc = InvalidScaleError("Q")
        assert "Q" in str(exc)

    def test_message_contains_valid_options(self):
        exc = InvalidScaleError("Q")
        msg = str(exc)
        assert "C" in msg and "F" in msg and "K" in msg

    def test_catchable_as_temperature_error(self):
        with pytest.raises(TemperatureError):
            raise InvalidScaleError("X")


class TestConvertTemperatureValid:

    @pytest.mark.parametrize("value,from_s,to_s,expected", [
        (100.0,  "C", "F", 212.0),
        (32.0,   "F", "C", 0.0),
        (0.0,    "C", "K", 273.15),
        (373.15, "K", "C", 100.0),
        (212.0,  "F", "K", 373.15),
        (373.15, "K", "F", 212.0),
        (0.0,    "C", "C", 0.0),    # same-scale no-op
        (100.0,  "F", "F", 100.0),  # same-scale no-op
    ])
    def test_conversions(self, value, from_s, to_s, expected):
        result = convert_temperature(value, from_s, to_s)
        assert result == pytest.approx(expected, abs=1e-3)

    def test_returns_float(self):
        result = convert_temperature(0.0, "C", "F")
        assert isinstance(result, float)

    def test_result_rounded_to_4_decimal_places(self):
        result = convert_temperature(1.0, "C", "F")
        # 1 °C = 33.8 °F — check rounding is applied
        assert result == round(result, 4)


class TestConvertTemperatureInvalidScale:

    def test_bad_from_scale_raises_invalid_scale_error(self):
        with pytest.raises(InvalidScaleError):
            convert_temperature(100.0, "X", "C")

    def test_bad_to_scale_raises_invalid_scale_error(self):
        with pytest.raises(InvalidScaleError):
            convert_temperature(100.0, "C", "Z")

    def test_lowercase_scale_is_invalid(self):
        with pytest.raises(InvalidScaleError):
            convert_temperature(100.0, "c", "F")

    def test_invalid_scale_exception_carries_scale(self):
        with pytest.raises(InvalidScaleError) as exc_info:
            convert_temperature(100.0, "Q", "C")
        assert exc_info.value.scale == "Q"


class TestConvertTemperatureBelowAbsoluteZero:

    def test_celsius_below_absolute_zero(self):
        with pytest.raises(BelowAbsoluteZeroError):
            convert_temperature(-274.0, "C", "F")

    def test_kelvin_below_zero(self):
        with pytest.raises(BelowAbsoluteZeroError):
            convert_temperature(-1.0, "K", "C")

    def test_fahrenheit_below_absolute_zero(self):
        # −460 °F ≈ −273.33 °C < absolute zero
        with pytest.raises(BelowAbsoluteZeroError):
            convert_temperature(-460.0, "F", "C")

    def test_exception_carries_celsius_value(self):
        with pytest.raises(BelowAbsoluteZeroError) as exc_info:
            convert_temperature(-300.0, "C", "F")
        assert exc_info.value.value_celsius == pytest.approx(-300.0)

    def test_exact_absolute_zero_does_not_raise(self):
        # −273.15 °C is valid (it IS absolute zero, not below it)
        result = convert_temperature(-273.15, "C", "K")
        assert result == pytest.approx(0.0, abs=1e-3)


# EXERCISE 2 — User Registry

class TestUserRegistryExceptionHierarchy:

    def test_already_exists_is_registry_error(self):
        assert issubclass(UserAlreadyExistsError, UserRegistryError)

    def test_not_found_is_registry_error(self):
        assert issubclass(UserNotFoundError, UserRegistryError)

    def test_registry_error_is_exception(self):
        assert issubclass(UserRegistryError, Exception)


class TestUserAlreadyExistsError:

    def test_stores_username(self):
        exc = UserAlreadyExistsError("alice")
        assert exc.username == "alice"

    def test_message_contains_username(self):
        exc = UserAlreadyExistsError("alice")
        assert "alice" in str(exc)

    def test_catchable_as_registry_error(self):
        with pytest.raises(UserRegistryError):
            raise UserAlreadyExistsError("alice")


class TestUserNotFoundError:

    def test_stores_username(self):
        exc = UserNotFoundError("bob")
        assert exc.username == "bob"

    def test_message_contains_username(self):
        exc = UserNotFoundError("bob")
        assert "bob" in str(exc)

    def test_catchable_as_registry_error(self):
        with pytest.raises(UserRegistryError):
            raise UserNotFoundError("bob")


class TestUserRegistryRegister:

    def setup_method(self):
        self.registry = UserRegistry()

    def test_register_new_user(self):
        self.registry.register("alice", "alice@example.com")
        assert self.registry.get_email("alice") == "alice@example.com"

    def test_register_duplicate_raises(self):
        self.registry.register("alice", "alice@example.com")
        with pytest.raises(UserAlreadyExistsError):
            self.registry.register("alice", "other@example.com")

    def test_register_case_insensitive_duplicate(self):
        self.registry.register("alice", "alice@example.com")
        with pytest.raises(UserAlreadyExistsError):
            self.registry.register("ALICE", "upper@example.com")

    def test_duplicate_exception_carries_username(self):
        self.registry.register("alice", "alice@example.com")
        with pytest.raises(UserAlreadyExistsError) as exc_info:
            self.registry.register("Alice", "other@example.com")
        assert exc_info.value.username == "alice"

    def test_username_stored_as_lowercase(self):
        self.registry.register("BOB", "bob@example.com")
        assert self.registry.get_email("bob") == "bob@example.com"


class TestUserRegistryGetEmail:

    def setup_method(self):
        self.registry = UserRegistry()
        self.registry.register("alice", "alice@example.com")

    def test_get_existing_user(self):
        assert self.registry.get_email("alice") == "alice@example.com"

    def test_get_is_case_insensitive(self):
        assert self.registry.get_email("ALICE") == "alice@example.com"

    def test_get_nonexistent_raises(self):
        with pytest.raises(UserNotFoundError):
            self.registry.get_email("nobody")

    def test_not_found_exception_carries_username(self):
        with pytest.raises(UserNotFoundError) as exc_info:
            self.registry.get_email("ghost")
        assert exc_info.value.username == "ghost"


class TestUserRegistryDelete:

    def setup_method(self):
        self.registry = UserRegistry()
        self.registry.register("alice", "alice@example.com")

    def test_delete_existing_user(self):
        self.registry.delete("alice")
        with pytest.raises(UserNotFoundError):
            self.registry.get_email("alice")

    def test_delete_case_insensitive(self):
        self.registry.delete("ALICE")
        with pytest.raises(UserNotFoundError):
            self.registry.get_email("alice")

    def test_delete_nonexistent_raises(self):
        with pytest.raises(UserNotFoundError):
            self.registry.delete("nobody")

    def test_after_delete_can_re_register(self):
        self.registry.delete("alice")
        self.registry.register("alice", "new@example.com")
        assert self.registry.get_email("alice") == "new@example.com"


class TestUserRegistryListUsers:

    def setup_method(self):
        self.registry = UserRegistry()

    def test_empty_registry(self):
        assert self.registry.list_users() == []

    def test_lists_registered_users(self):
        self.registry.register("charlie", "c@x.com")
        self.registry.register("alice", "a@x.com")
        self.registry.register("bob", "b@x.com")
        assert self.registry.list_users() == ["alice", "bob", "charlie"]

    def test_list_is_sorted(self):
        self.registry.register("zebra", "z@x.com")
        self.registry.register("apple", "a@x.com")
        users = self.registry.list_users()
        assert users == sorted(users)

    def test_list_is_lowercase(self):
        self.registry.register("DAVE", "dave@x.com")
        assert "dave" in self.registry.list_users()



# EXERCISE 3 — Pipeline with Exception Chaining

class TestPipelineExceptionHierarchy:

    def test_pipeline_error_is_exception(self):
        assert issubclass(PipelineError, Exception)

    def test_parse_error_is_pipeline_error(self):
        assert issubclass(ParseError, PipelineError)

    def test_process_error_is_pipeline_error(self):
        assert issubclass(ProcessError, PipelineError)


class TestPipelineError:

    def test_stores_raw(self):
        exc = PipelineError("oops", raw="bad input")
        assert exc.raw == "bad input"

    def test_message(self):
        exc = PipelineError("oops", raw="bad input")
        assert "oops" in str(exc)


class TestProcessError:

    def test_stores_raw_and_field(self):
        exc = ProcessError("bad age", raw="alice,-1,50", field="age")
        assert exc.raw == "alice,-1,50"
        assert exc.field == "age"

    def test_catchable_as_pipeline_error(self):
        with pytest.raises(PipelineError):
            raise ProcessError("bad age", raw="x", field="age")


class TestParseRecord:

    def test_valid_record(self):
        result = parse_record("Alice,25,87.5")
        assert result == {"name": "Alice", "age": 25, "score": 87.5}

    def test_age_is_int(self):
        result = parse_record("Bob,30,60.0")
        assert isinstance(result["age"], int)

    def test_score_is_float(self):
        result = parse_record("Bob,30,60.0")
        assert isinstance(result["score"], float)

    def test_too_few_fields_raises_parse_error(self):
        with pytest.raises(ParseError):
            parse_record("Alice,25")

    def test_too_many_fields_raises_parse_error(self):
        with pytest.raises(ParseError):
            parse_record("Alice,25,87.5,extra")

    def test_non_integer_age_raises_parse_error(self):
        with pytest.raises(ParseError):
            parse_record("Alice,abc,87.5")

    def test_non_float_score_raises_parse_error(self):
        with pytest.raises(ParseError):
            parse_record("Alice,25,xyz")

    def test_parse_error_carries_raw(self):
        raw = "bad,input"
        with pytest.raises(ParseError) as exc_info:
            parse_record(raw)
        assert exc_info.value.raw == raw


class TestProcessRecord:

    def _make_raw(self):
        return "Alice,25,87.5"

    def test_valid_record_returns_dict(self):
        record = {"name": "Alice", "age": 25, "score": 87.5}
        result = process_record(record, self._make_raw())
        assert result["name"] == "Alice"
        assert result["age"] == 25
        assert result["score"] == 87.5

    @pytest.mark.parametrize("score,expected_grade", [
        (95.0, "A"),
        (90.0, "A"),
        (89.9, "B"),
        (75.0, "B"),
        (74.9, "C"),
        (60.0, "C"),
        (59.9, "D"),
        (45.0, "D"),
        (44.9, "F"),
        (0.0,  "F"),
    ])
    def test_grade_assignment(self, score, expected_grade):
        record = {"name": "Alice", "age": 25, "score": score}
        result = process_record(record, self._make_raw())
        assert result["grade"] == expected_grade

    def test_empty_name_raises_process_error(self):
        with pytest.raises(ProcessError) as exc_info:
            process_record({"name": "", "age": 25, "score": 50.0}, "")
        assert exc_info.value.field == "name"

    def test_negative_age_raises_process_error(self):
        with pytest.raises(ProcessError) as exc_info:
            process_record({"name": "Alice", "age": -1, "score": 50.0}, "")
        assert exc_info.value.field == "age"

    def test_age_over_150_raises_process_error(self):
        with pytest.raises(ProcessError) as exc_info:
            process_record({"name": "Alice", "age": 151, "score": 50.0}, "")
        assert exc_info.value.field == "age"

    def test_score_below_0_raises_process_error(self):
        with pytest.raises(ProcessError) as exc_info:
            process_record({"name": "Alice", "age": 25, "score": -1.0}, "")
        assert exc_info.value.field == "score"

    def test_score_above_100_raises_process_error(self):
        with pytest.raises(ProcessError) as exc_info:
            process_record({"name": "Alice", "age": 25, "score": 100.1}, "")
        assert exc_info.value.field == "score"

    def test_boundary_age_0_is_valid(self):
        record = {"name": "Alice", "age": 0, "score": 50.0}
        result = process_record(record, "")
        assert result["age"] == 0

    def test_boundary_age_150_is_valid(self):
        record = {"name": "Alice", "age": 150, "score": 50.0}
        result = process_record(record, "")
        assert result["age"] == 150

    def test_process_error_carries_raw(self):
        raw = "Alice,-1,50"
        with pytest.raises(ProcessError) as exc_info:
            process_record({"name": "Alice", "age": -1, "score": 50.0}, raw)
        assert exc_info.value.raw == raw


class TestRunPipeline:

    def test_valid_input_returns_dict(self):
        result = run_pipeline("Alice,25,87.5")
        assert result["name"] == "Alice"
        assert result["grade"] == "B"

    def test_parse_failure_raises_pipeline_error(self):
        with pytest.raises(PipelineError):
            run_pipeline("bad,input")

    def test_process_failure_raises_pipeline_error(self):
        with pytest.raises(PipelineError):
            run_pipeline("Alice,-5,50.0")

    def test_parse_error_is_chained(self):
        """The PipelineError raised must chain the original ParseError."""
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline("no,commas,at,all,here")
        assert isinstance(exc_info.value.__cause__, ParseError)

    def test_process_error_is_chained(self):
        """The PipelineError raised must chain the original ProcessError."""
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline("Alice,200,50.0")   # age > 150
        assert isinstance(exc_info.value.__cause__, ProcessError)

    def test_pipeline_error_carries_raw(self):
        raw = "garbage,data"
        with pytest.raises(PipelineError) as exc_info:
            run_pipeline(raw)
        assert exc_info.value.raw == raw

    @pytest.mark.parametrize("raw,expected_name,expected_grade", [
        ("Zoe,22,95",   "Zoe",   "A"),
        ("Tom,40,75",   "Tom",   "B"),
        ("Eve,30,60",   "Eve",   "C"),
        ("Max,18,45",   "Max",   "D"),
        ("Ivy,55,0",    "Ivy",   "F"),
    ])
    def test_various_valid_inputs(self, raw, expected_name, expected_grade):
        result = run_pipeline(raw)
        assert result["name"] == expected_name
        assert result["grade"] == expected_grade
