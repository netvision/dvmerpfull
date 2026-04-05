"""
tests/test_xlsx_parser.py
Tests for the xlsx_parser module.
Run with: venv/Scripts/pytest tests/ -v
"""
import os
import sys
import pytest

# Ensure the backend directory is on the path so xlsx_parser can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xlsx_parser import parse_xlsx, _normalize_exhibit_ref, _strip_aim_prefix, _clean

# ---------------------------------------------------------------------------
# Paths to test xlsx files (relative to the project root D:/dvm/lessons/)
# ---------------------------------------------------------------------------
LESSONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

FILES = {
    "english_chapter": os.path.join(LESSONS_DIR, "class6_english_chapter1.xlsx"),
    "english_poem":    os.path.join(LESSONS_DIR, "class6_english_poem1.xlsx"),
    "sst":             os.path.join(LESSONS_DIR, "class6_sst_chapter1.xlsx"),
    "science":         os.path.join(LESSONS_DIR, "class6_science_chapter1.xlsx"),
    "hindi":           os.path.join(LESSONS_DIR, "class6_hindi_chapter1.xlsx"),
    "maths":           os.path.join(LESSONS_DIR, "class6-maths-chapter1.xlsx"),
}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _parse(key: str) -> dict:
    return parse_xlsx(FILES[key])


# ---------------------------------------------------------------------------
# Tests: parse_xlsx — no exceptions & basic structure
# ---------------------------------------------------------------------------

class TestParseNoExceptions:
    def test_english_chapter_parses(self):
        result = _parse("english_chapter")
        assert isinstance(result, dict)

    def test_english_poem_parses(self):
        result = _parse("english_poem")
        assert isinstance(result, dict)

    def test_sst_parses(self):
        result = _parse("sst")
        assert isinstance(result, dict)

    def test_science_parses(self):
        result = _parse("science")
        assert isinstance(result, dict)

    def test_hindi_parses(self):
        result = _parse("hindi")
        assert isinstance(result, dict)

    def test_maths_parses(self):
        result = _parse("maths")
        assert isinstance(result, dict)


class TestOutputStructure:
    """Every result must have the required top-level keys."""

    @pytest.mark.parametrize("key", list(FILES.keys()))
    def test_has_required_keys(self, key):
        result = _parse(key)
        assert "title" in result
        assert "aim" in result
        assert "concepts" in result
        assert "exhibits" in result

    @pytest.mark.parametrize("key", list(FILES.keys()))
    def test_concepts_are_list(self, key):
        result = _parse(key)
        assert isinstance(result["concepts"], list)

    @pytest.mark.parametrize("key", list(FILES.keys()))
    def test_exhibits_are_dict(self, key):
        result = _parse(key)
        assert isinstance(result["exhibits"], dict)


# ---------------------------------------------------------------------------
# Tests: chapter titles are non-empty
# ---------------------------------------------------------------------------

class TestChapterTitle:
    @pytest.mark.parametrize("key", list(FILES.keys()))
    def test_title_nonempty(self, key):
        result = _parse(key)
        assert result["title"], f"title is empty for {key}"

    def test_english_chapter_title_content(self):
        result = _parse("english_chapter")
        assert "Bottle of Dew" in result["title"] or "Fables" in result["title"]

    def test_english_poem_title_content(self):
        result = _parse("english_poem")
        assert "Raven" in result["title"] or "Poem" in result["title"]

    def test_sst_title_content(self):
        result = _parse("sst")
        assert "Social Science" in result["title"] or "Locating" in result["title"]

    def test_science_title_content(self):
        result = _parse("science")
        assert "Science" in result["title"] or "science" in result["title"].lower()

    def test_hindi_title_nonempty(self):
        result = _parse("hindi")
        assert len(result["title"]) > 5

    def test_maths_title_content(self):
        result = _parse("maths")
        assert "Pattern" in result["title"] or "Maths" in result["title"] or "Mathematics" in result["title"]


# ---------------------------------------------------------------------------
# Tests: at least one concept per file
# ---------------------------------------------------------------------------

class TestConcepts:
    @pytest.mark.parametrize("key", list(FILES.keys()))
    def test_at_least_one_concept(self, key):
        result = _parse(key)
        assert len(result["concepts"]) >= 1, f"No concepts parsed for {key}"

    def test_english_chapter_has_3_concepts(self):
        result = _parse("english_chapter")
        assert len(result["concepts"]) == 3

    def test_english_poem_has_3_concepts(self):
        result = _parse("english_poem")
        assert len(result["concepts"]) == 3

    def test_sst_has_4_concepts(self):
        result = _parse("sst")
        assert len(result["concepts"]) == 4

    def test_science_has_7_concepts(self):
        result = _parse("science")
        assert len(result["concepts"]) == 7

    def test_hindi_has_3_concepts(self):
        result = _parse("hindi")
        assert len(result["concepts"]) == 3

    def test_maths_has_2_concepts(self):
        result = _parse("maths")
        assert len(result["concepts"]) == 2

    def test_concept_has_required_fields(self):
        result = _parse("english_chapter")
        for concept in result["concepts"]:
            assert "s_no" in concept
            assert "title" in concept
            assert "sessions" in concept
            assert "exhibit_ref" in concept
            assert "learning_outcomes" in concept
            assert "integration_other_sub" in concept
            assert "library" in concept
            assert "activity" in concept
            assert "life_lesson" in concept
            assert "remarks" in concept

    def test_concept_values_are_strings(self):
        result = _parse("english_chapter")
        for concept in result["concepts"]:
            for k, v in concept.items():
                assert isinstance(v, str), f"Concept field '{k}' should be str, got {type(v)}"

    def test_science_concepts_have_sno_fallback(self):
        """Science has no s_no column — falls back to row index."""
        result = _parse("science")
        for concept in result["concepts"]:
            assert concept["s_no"] != "", "s_no should not be empty (fallback to row index)"

    def test_science_concepts_have_titles(self):
        result = _parse("science")
        titles = [c["title"] for c in result["concepts"]]
        assert "Curiosity and science" in titles
        assert "what is science" in titles


# ---------------------------------------------------------------------------
# Tests: exhibit_ref normalization
# ---------------------------------------------------------------------------

class TestExhibitRefNormalization:
    def test_exhibit_1_normalized(self):
        assert _normalize_exhibit_ref("Exhibit 1") == "exhibit_1"

    def test_exhibit_1_lowercase(self):
        assert _normalize_exhibit_ref("exhibit 1") == "exhibit_1"

    def test_exhibit_1_no_space(self):
        assert _normalize_exhibit_ref("Exhibit1") == "exhibit_1"

    def test_exhibits_2_cell_ref(self):
        assert _normalize_exhibit_ref("'Exhibits 2'!B1") == "exhibit_2"

    def test_exhibit_2_lowercase(self):
        assert _normalize_exhibit_ref("exhibit 2") == "exhibit_2"

    def test_empty_string_returns_empty(self):
        assert _normalize_exhibit_ref("") == ""

    def test_none_returns_empty(self):
        assert _normalize_exhibit_ref(None) == ""

    def test_concepts_have_normalized_refs(self):
        """All non-empty exhibit_refs in parsed concepts should be 'exhibit_N' form."""
        import re
        for key in FILES:
            result = _parse(key)
            for concept in result["concepts"]:
                ref = concept["exhibit_ref"]
                if ref:
                    assert re.match(r'^exhibit_\d+$', ref), \
                        f"exhibit_ref {ref!r} not normalized in {key}"

    def test_english_chapter_concepts_have_exhibit_refs(self):
        result = _parse("english_chapter")
        assert result["concepts"][0]["exhibit_ref"] == "exhibit_1"
        assert result["concepts"][1]["exhibit_ref"] == "exhibit_2"
        assert result["concepts"][2]["exhibit_ref"] == "exhibit_3"

    def test_sst_concepts_have_exhibit_refs(self):
        result = _parse("sst")
        refs = [c["exhibit_ref"] for c in result["concepts"]]
        assert "exhibit_1" in refs
        assert "exhibit_2" in refs
        assert "exhibit_3" in refs
        assert "exhibit_4" in refs


# ---------------------------------------------------------------------------
# Tests: aim prefix stripped
# ---------------------------------------------------------------------------

class TestAimPrefixStripped:
    @pytest.mark.parametrize("key", list(FILES.keys()))
    def test_aim_nonempty(self, key):
        result = _parse(key)
        assert result["aim"], f"aim is empty for {key}"

    def test_english_chapter_aim_no_prefix(self):
        result = _parse("english_chapter")
        aim = result["aim"]
        assert not aim.startswith("Aim:"), f"aim still has 'Aim:' prefix: {aim[:40]!r}"
        assert not aim.startswith("Aim-"), f"aim still has 'Aim-' prefix: {aim[:40]!r}"
        assert not aim.lower().startswith("aim"), f"aim still starts with 'aim': {aim[:40]!r}"

    def test_english_poem_aim_no_prefix(self):
        result = _parse("english_poem")
        aim = result["aim"]
        assert not aim.lower().startswith("aim"), f"aim still starts with 'aim': {aim[:40]!r}"

    def test_sst_aim_no_prefix(self):
        result = _parse("sst")
        aim = result["aim"]
        assert not aim.lower().startswith("aim"), f"aim still starts with 'aim': {aim[:40]!r}"

    def test_science_aim_no_prefix(self):
        result = _parse("science")
        aim = result["aim"]
        assert not aim.lower().startswith("aim"), f"aim still starts with 'aim': {aim[:40]!r}"

    def test_maths_aim_no_prefix(self):
        result = _parse("maths")
        aim = result["aim"]
        assert not aim.lower().startswith("aim"), f"aim still starts with 'aim': {aim[:40]!r}"

    def test_strip_aim_function_colon(self):
        assert _strip_aim_prefix("Aim: Some text") == "Some text"

    def test_strip_aim_function_dash(self):
        assert _strip_aim_prefix("Aim-Some text") == "Some text"

    def test_strip_aim_function_colon_dash(self):
        assert _strip_aim_prefix("Aim: -Some text") == "Some text"

    def test_strip_aim_function_colondashadj(self):
        assert _strip_aim_prefix("Aim:-Some text") == "Some text"

    def test_strip_aim_function_uppercase(self):
        assert _strip_aim_prefix("AIM: Some text") == "Some text"


# ---------------------------------------------------------------------------
# Tests: exhibits parsed
# ---------------------------------------------------------------------------

class TestExhibits:
    @pytest.mark.parametrize("key", list(FILES.keys()))
    def test_at_least_one_exhibit(self, key):
        result = _parse(key)
        assert len(result["exhibits"]) >= 1, f"No exhibits for {key}"

    def test_exhibit_has_raw_title_and_fields(self):
        result = _parse("english_chapter")
        for ex_key, ex_val in result["exhibits"].items():
            assert "raw_title" in ex_val, f"Missing raw_title in {ex_key}"
            assert "fields" in ex_val, f"Missing fields in {ex_key}"
            assert isinstance(ex_val["fields"], dict), f"fields not a dict in {ex_key}"

    def test_english_exhibit1_has_english_fields(self):
        result = _parse("english_chapter")
        fields = result["exhibits"]["exhibit_1"]["fields"]
        assert "about_chapter" in fields
        assert "chapter_overview" in fields
        assert "link" in fields

    def test_english_exhibit1_about_chapter_nonempty(self):
        result = _parse("english_chapter")
        fields = result["exhibits"]["exhibit_1"]["fields"]
        assert fields["about_chapter"].strip() != ""

    def test_english_exhibit2_has_grammar_fields(self):
        result = _parse("english_chapter")
        fields = result["exhibits"]["exhibit_2"]["fields"]
        assert "grammar_topic" in fields

    def test_poem_exhibit3_has_assessment_fields(self):
        result = _parse("english_poem")
        fields = result["exhibits"]["exhibit_3"]["fields"]
        assert "very_short_answers" in fields
        assert "short_answers" in fields
        assert "long_answers" in fields

    def test_science_exhibits_have_science_fields(self):
        result = _parse("science")
        for ex_key, ex_val in result["exhibits"].items():
            fields = ex_val["fields"]
            assert "intro_questions" in fields, f"Missing intro_questions in {ex_key}"
            assert "explanation" in fields, f"Missing explanation in {ex_key}"

    def test_sst_exhibit1_has_fields(self):
        result = _parse("sst")
        ex = result["exhibits"]["exhibit_1"]
        assert ex["raw_title"] != ""
        # SST exhibit 1 is science-type
        assert len(ex["fields"]) > 0

    def test_hindi_exhibits_normalized_keys(self):
        """Hindi Sheet4 should map to exhibit_3, not exhibit_4."""
        result = _parse("hindi")
        assert "exhibit_3" in result["exhibits"], \
            f"exhibit_3 missing; got keys: {list(result['exhibits'].keys())}"
        assert "exhibit_4" not in result["exhibits"], \
            f"exhibit_4 should not exist; Sheet4 contains Exhibit 3"

    def test_exhibit_field_values_are_strings(self):
        """All field values must be strings."""
        for key in FILES:
            result = _parse(key)
            for ex_key, ex_val in result["exhibits"].items():
                for fk, fv in ex_val["fields"].items():
                    assert isinstance(fv, str), \
                        f"Field {fk!r} in {ex_key} of {key} is not str: {type(fv)}"

    def test_maths_exhibits_have_science_type_fields(self):
        result = _parse("maths")
        for ex_key, ex_val in result["exhibits"].items():
            fields = ex_val["fields"]
            assert "intro_questions" in fields or "explanation" in fields, \
                f"Expected science-type fields in {ex_key}: got {list(fields.keys())}"


# ---------------------------------------------------------------------------
# Tests: _clean helper
# ---------------------------------------------------------------------------

class TestClean:
    def test_none_returns_empty_string(self):
        assert _clean(None) == ""

    def test_strips_whitespace(self):
        assert _clean("  hello  ") == "hello"

    def test_int_to_string(self):
        assert _clean(42) == "42"

    def test_empty_string_unchanged(self):
        assert _clean("") == ""

    def test_preserves_newlines(self):
        assert _clean("line1\nline2") == "line1\nline2"


# ---------------------------------------------------------------------------
# Tests: Hindi Unicode support
# ---------------------------------------------------------------------------

class TestHindiUnicode:
    def test_hindi_title_contains_unicode(self):
        result = _parse("hindi")
        # Hindi title should contain Devanagari characters
        assert any(ord(c) > 127 for c in result["title"]), \
            "Hindi title should contain non-ASCII characters"

    def test_hindi_concepts_have_unicode_titles(self):
        result = _parse("hindi")
        for concept in result["concepts"]:
            assert isinstance(concept["title"], str)
        # First concept title should be in Hindi
        first_title = result["concepts"][0]["title"]
        assert any(ord(c) > 127 for c in first_title), \
            f"First Hindi concept title should have Devanagari: {first_title!r}"
