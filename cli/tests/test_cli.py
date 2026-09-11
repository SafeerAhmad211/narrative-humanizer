import json

import pytest

import narrative_humanizer.cli as cli_module
from narrative_humanizer.analyzer import AxisResult
from narrative_humanizer.checklist import CHECKLIST


def test_check_reports_error_for_missing_file(capsys):
    exit_code = cli_module.main(["check", "does-not-exist.txt"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "no such file" in captured.err


def test_check_markdown_output(tmp_path, monkeypatch, capsys):
    story = tmp_path / "story.txt"
    story.write_text("Once upon a time...", encoding="utf-8")

    fake_results = [
        AxisResult(id=CHECKLIST[0].id, ai_leaning_present=True, evidence="quote", suggested_edit="fix it"),
    ]
    monkeypatch.setattr(cli_module, "analyze_story", lambda text, model: fake_results)

    exit_code = cli_module.main(["check", str(story)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "story" in captured.out  # story.stem used as report title
    assert CHECKLIST[0].name in captured.out


def test_check_json_output(tmp_path, monkeypatch, capsys):
    story = tmp_path / "story.txt"
    story.write_text("Once upon a time...", encoding="utf-8")

    fake_results = [
        AxisResult(id=CHECKLIST[0].id, ai_leaning_present=False, evidence="", suggested_edit=""),
    ]
    monkeypatch.setattr(cli_module, "analyze_story", lambda text, model: fake_results)

    exit_code = cli_module.main(["check", str(story), "--format", "json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload == [
        {
            "id": CHECKLIST[0].id,
            "ai_leaning_present": False,
            "evidence": "",
            "suggested_edit": "",
        }
    ]


def test_check_surfaces_analyzer_runtime_error(tmp_path, monkeypatch, capsys):
    story = tmp_path / "story.txt"
    story.write_text("Once upon a time...", encoding="utf-8")

    def _raise(text, model):
        raise RuntimeError("Set the ANTHROPIC_API_KEY environment variable to run analysis.")

    monkeypatch.setattr(cli_module, "analyze_story", _raise)

    exit_code = cli_module.main(["check", str(story)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "ANTHROPIC_API_KEY" in captured.err


def test_list_checklist_prints_every_axis(capsys):
    exit_code = cli_module.main(["list-checklist"])
    captured = capsys.readouterr()
    assert exit_code == 0
    for item in CHECKLIST:
        assert item.id in captured.out
        assert item.name in captured.out


def test_no_command_exits_nonzero():
    with pytest.raises(SystemExit):
        cli_module.main([])


def test_default_model_is_claude_sonnet_5():
    parser = cli_module.build_parser()
    args = parser.parse_args(["check", "story.txt"])
    assert args.model == "claude-sonnet-5"
