import pytest
import project
from unittest import mock


@mock.patch('subprocess.run')
def test_upgrade_database(mock_subprocess_run):
    project.upgrade_database()
    mock_subprocess_run.assert_any_call(['alembic', 'upgrade', 'head'])

def test_check_database_version():
    res = project.check_database_version()
    assert ('(head)' in  res) == True


@mock.patch('subprocess.run')
def test_start_app(mock_subprocess_run):
    project.start_app()
    mock_subprocess_run.assert_any_call(['uvicorn', 'app.main:app', '--host', 'localhost', '--port', '8000'])
