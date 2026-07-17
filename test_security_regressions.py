import re
from pathlib import Path


def test_context_menu_values_escape_javascript() -> None:
    template = (Path(__file__).parent / "awssecurityhub_get_findings.html").read_text()
    values = re.findall(r"context_menu\(.*?'value'\s*:\s*'\s*({{.*?}})", template)

    assert values
    assert all("|escapejs" in value for value in values)


def test_pagination_is_bounded_and_requires_token_progress() -> None:
    connector = (Path(__file__).parent / "awssecurityhub_connector.py").read_text()

    assert "AWSSECURITYHUB_MAX_PAGINATION_PAGES" in connector
    assert "AWSSECURITYHUB_MAX_PAGINATION_ITEMS" in connector
    assert "next_token in seen_tokens" in connector


def test_checkpoint_advances_only_after_durable_ingestion() -> None:
    connector = (Path(__file__).parent / "awssecurityhub_connector.py").read_text()
    handler = connector.split("def _handle_on_poll", 1)[1].split("def _handle_get_findings", 1)[0]

    assert handler.index("artifacts_creation_status") < handler.index('self._state["last_ingested_date"]')
    assert "last_successful_updated_at" in handler
    assert "datetime.now(timezone.utc)" in connector


def test_sqs_deletion_follows_successful_ingestion() -> None:
    connector = (Path(__file__).parent / "awssecurityhub_connector.py").read_text()
    fetcher = connector.split("def _poll_from_sqs", 1)[1].split("def _poll_from_security_hub", 1)[0]
    handler = connector.split("def _handle_on_poll", 1)[1].split("def _handle_get_findings", 1)[0]

    assert '"delete_message"' not in fetcher
    assert handler.index("successful_finding_ids.add") < handler.index('"delete_message"')
