import pytest
from hbutils.testing import simulate_entry

from ghutils.config.meta import __VERSION__
from ghutils.entry import ghutilscli


@pytest.mark.unittest
class TestEntryDispatch:
    def test_version(self):
        result = simulate_entry(ghutilscli, ['ghutils', '-v'])
        assert result.exitcode == 0
        assert __VERSION__ in result.stdout
