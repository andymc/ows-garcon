from __future__ import absolute_import
try:
    from unittest.mock import MagicMock
except:  # noqa: E722
    from mock import MagicMock
import boto.swf.layer2 as swf

from garcon import context


def mock(monkeypatch):
    for base in [swf.Decider, swf.WorkflowType, swf.ActivityType, swf.Domain]:
        monkeypatch.setattr(base, '__init__', MagicMock(return_value=None))
        if base is not swf.Decider:
            monkeypatch.setattr(base, 'register', MagicMock())


def test_context_creation_without_events(monkeypatch):
    """Check the basic context creation.
    """

    mock(monkeypatch)
    current_context = context.ExecutionContext()
    assert not current_context.current
    assert not current_context.workflow_input


def test_context_creation_with_events(monkeypatch):
    """Test context creation with events.
    """

    mock(monkeypatch)
    from tests.fixtures import decider as poll

    current_context = context.ExecutionContext(poll.history.get('events'))
    assert current_context.current == {'k': 'v'}


def test_get_workflow_execution_info(monkeypatch):
    """Check that the workflow execution info are properly extracted
    """

    mock(monkeypatch)
    from tests.fixtures import decider as poll

    current_context = context.ExecutionContext()
    current_context.set_workflow_execution_info(poll.history, 'dev')

    # Test extracting workflow execution info
    assert current_context.current == {
        'execution.domain': 'dev',
        'execution.run_id': '123abc=',
        'execution.workflow_id': 'test-workflow-id'}
