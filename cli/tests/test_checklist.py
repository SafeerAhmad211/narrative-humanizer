from narrative_humanizer.checklist import CHECKLIST, MODEL_FINGERPRINTS


def test_checklist_ids_are_unique():
    ids = [item.id for item in CHECKLIST]
    assert len(ids) == len(set(ids))


def test_checklist_items_have_all_fields():
    for item in CHECKLIST:
        assert item.name
        assert item.ai_default
        assert item.human_leaning
        assert item.fix
        assert item.stat


def test_model_fingerprints_cover_five_models():
    assert set(MODEL_FINGERPRINTS) == {"claude", "gpt", "gemini", "deepseek", "kimi"}
