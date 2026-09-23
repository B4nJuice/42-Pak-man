import pytest

from src.config.config_manager import ConfigManager


@pytest.fixture
def manager() -> ConfigManager:
    manager = object.__new__(ConfigManager)
    manager._init_formater()
    return manager


@pytest.mark.parametrize(
    ('source', 'expected'),
    [
        (
            ['{"value": "#tag // path /* text */"} # comment\n'],
            ['{"value": "#tag // path /* text */"} ']
        ),
        (
            ['{"value": "escaped \\" // still text"} // comment\n'],
            ['{"value": "escaped \\" // still text"} ']
        ),
        (
            ['{"value": 1 /* comment */}\n'],
            ['{"value": 1 }\n']
        ),
        (
            ['{"value": 1 /* c\n', 'omment */}\n'],
            ['{"value": 1 ', '}\n']
        ),
        (
            ['{"value": 1 /* //c\n', 'omment */}\n'],
            ['{"value": 1 ', '}\n']
        ),
        (
            ['{"value": 1 /* /* //c\n', 'omment */*/}\n'],
            ['{"value": 1 ', '*/}\n']
        ),
    ],
)
def test_format_line_removes_comments_outside_strings(
    manager: ConfigManager,
    source: list[str],
    expected: list[str],
) -> None:
    for s, e in zip(source, expected):
        assert manager._format_line(s) == e


@pytest.mark.parametrize(
    ('source', 'expected'),
    [
        ('{"value": "/*"}\n', '{"value": "/*"}\n'),
        ('{"value": 1 /* open\n', '{"value": 1 '),
        ('still comment */}\n', 'still comment */}\n'),
    ],
)
def test_format_line_handles_block_comment_edges(
    manager: ConfigManager,
    source: str,
    expected: str,
) -> None:
    assert manager._format_line(source) == expected


def test_loads_config_from_file(tmp_path) -> None:
    config_path = tmp_path / 'config.jsonc'
    config_path.write_text('{"highscore_path": "scores.json"}\n')

    manager = ConfigManager(str(config_path))

    assert manager.get_config().highscore_path == 'scores.json'


def test_missing_config_raises_file_not_found(tmp_path) -> None:
    config_path = tmp_path / 'missing.jsonc'

    with pytest.raises(FileNotFoundError, match='Config file not found'):
        ConfigManager(str(config_path))


def test_invalid_config_raises_runtime_error(tmp_path) -> None:
    config_path = tmp_path / 'config.jsonc'
    config_path.write_text('{ invalid json }')

    with pytest.raises(RuntimeError, match='Failed to parse config'):
        ConfigManager(str(config_path))
