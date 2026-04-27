import os
import pytest
from unittest.mock import patch, MagicMock

os.environ.setdefault("DUCKDNS_TOKEN", "test-token")
os.environ.setdefault("DUCKDNS_DOMAIN", "cbcloud")

import ip


def mock_response(text):
    r = MagicMock()
    r.text = text
    return r


class TestGetIp:
    def test_returns_ip(self):
        with patch("ip.requests.get", return_value=mock_response("1.2.3.4")) as m:
            assert ip.get_ip() == "1.2.3.4"
            m.assert_called_once_with("https://api.ipify.org", timeout=10)

    def test_returns_none_on_exception(self):
        with patch("ip.requests.get", side_effect=Exception("timeout")):
            assert ip.get_ip() is None


class TestUpdateDuckdns:
    def test_logs_ok_on_success(self, caplog):
        import logging
        with caplog.at_level(logging.INFO), patch("ip.requests.get", return_value=mock_response("OK\n...")):
            ip.update_duckdns("1.2.3.4")
        assert "updated" in caplog.text

    def test_logs_error_on_failure(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR), patch("ip.requests.get", return_value=mock_response("KO")):
            ip.update_duckdns("1.2.3.4")
        assert "failed" in caplog.text

    def test_uses_https(self):
        with patch("ip.requests.get", return_value=mock_response("OK")) as m:
            ip.update_duckdns("1.2.3.4")
            url = m.call_args[0][0]
            assert url.startswith("https://")
            assert "1.2.3.4" in url
            assert "cbcloud" in url


@pytest.mark.integration
class TestIntegration:
    """Requires real DUCKDNS_TOKEN env var. Run with: pytest -m integration"""

    def test_real_duckdns_update(self):
        token = os.environ.get("DUCKDNS_TOKEN", "")
        if not token or token == "test-token":
            pytest.skip("no real token")
        current_ip = ip.get_ip()
        assert current_ip is not None
        with patch("ip.requests.get", wraps=ip.requests.get) as m:
            ip.update_duckdns(current_ip)
            url = m.call_args[0][0]
            resp = ip.requests.get(url, timeout=10)
            assert resp.text.startswith("OK")
