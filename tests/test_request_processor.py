from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from aspen.request_processor import RequestProcessor


def test_basic():
    rp = RequestProcessor()
    expected = os.getcwd()
    actual = rp.www_root
    assert actual == expected

def test_processor_can_process(harness):
    output = harness.simple('[---]\n[---]\nGreetings, program!', 'index.html.spt')
    assert output.text == 'Greetings, program!'

def test_user_can_influence_render_context_via_algorithm_state(harness):
    def add_foo_to_context(path):
        return {'foo': 'bar'}
    harness.request_processor.algorithm.insert_after('dispatch_path_to_filesystem', add_foo_to_context)
    assert harness.simple('[---]\n[---]\n%(foo)s', 'index.html.spt').text == 'bar'

def test_resources_can_import_from_project_root(harness):
    harness.fs.project.mk(('foo.py', 'bar = "baz"'))
    assert harness.simple( "from foo import bar\n[---]\n[---]\nGreetings, %(bar)s!"
                         , 'index.html.spt'
                         , raise_immediately=False).text == "Greetings, baz!"
