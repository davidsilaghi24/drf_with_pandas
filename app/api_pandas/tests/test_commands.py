"""
Test custom Django Management commands.
"""
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2Error


@patch("api_pandas.management.commands.wait_for_db.Command.check")
class CommandTest(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    def test_wait_for_db_delay(self, patched_check):
        """Test waiting for database when getting operational error."""
        patched_check.side_effect = [
            Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
