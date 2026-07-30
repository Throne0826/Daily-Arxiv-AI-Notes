from daily_arxiv_notes.config import load_settings


def test_project_env_takes_precedence_for_llm_settings(tmp_path, monkeypatch) -> None:
    (tmp_path / "taxonomy.json").write_text('{"groups": {}, "categories": {}}')
    (tmp_path / "config.toml").write_text(
        '[project]\ntaxonomy_file = "taxonomy.json"\n'
        '[llm]\nmodel_env = "OPENAI_MODEL"\napi_key_env = "OPENAI_API_KEY"\n',
        encoding="utf-8",
    )
    (tmp_path / ".env").write_text(
        'OPENAI_MODEL="file-model"\nOPENAI_API_KEY=secret\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENAI_MODEL", "process-model")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    settings = load_settings(tmp_path / "config.toml")

    assert settings.llm_value("model") == "file-model"
    assert settings.llm_value("api_key") == "secret"
