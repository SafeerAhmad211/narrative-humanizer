from narrative_humanizer.analyzer import AxisResult
from narrative_humanizer.checklist import CHECKLIST
from narrative_humanizer.report import to_markdown


def test_report_separates_flagged_and_clean_axes():
    results = [
        AxisResult(id=CHECKLIST[0].id, ai_leaning_present=True, evidence="quote", suggested_edit="do X"),
        AxisResult(id=CHECKLIST[1].id, ai_leaning_present=False, evidence="", suggested_edit=""),
    ]
    md = to_markdown(results, story_name="test-story")

    assert "test-story" in md
    assert "1 of 2 checklist axes" in md
    assert CHECKLIST[0].name in md
    assert "quote" in md
    assert "Axes already human-leaning" in md
    assert CHECKLIST[1].name in md


def test_report_falls_back_to_default_fix_when_no_suggested_edit():
    results = [
        AxisResult(id=CHECKLIST[0].id, ai_leaning_present=True, evidence="whole-story", suggested_edit=""),
    ]
    md = to_markdown(results)
    assert CHECKLIST[0].fix in md


def test_report_surfaces_unrecognized_flagged_axis_instead_of_dropping_it():
    # A hallucinated or typo'd axis id from the model must still show up in the
    # report -- silently dropping a flagged finding would hide a real result.
    results = [
        AxisResult(id="not_a_real_axis", ai_leaning_present=True, evidence="odd quote", suggested_edit="do something"),
    ]
    md = to_markdown(results)
    assert "not_a_real_axis" in md
    assert "odd quote" in md
    assert "do something" in md
    assert "1 of 1 checklist axes" in md
