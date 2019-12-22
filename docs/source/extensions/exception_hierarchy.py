"""Credits to Github user Rapptz (Danny)"""
from docutils.parsers.rst import Directive
from docutils import nodes


class exception_hierarchy(nodes.General, nodes.Element):
    pass


def visit_html_exception_hierarchy_node(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='exception-hierarchy-content'))


def depart_html_exception_hierarchy_node(self, node):
    self.body.append('\n')


def visit_any_exception_hierarchy_node(self, node):
    self.visit_paragraph(node)


def depart_any_exception_hierarchy_node(self, node):
    self.depart_paragraph(node)


class ExceptionHierarchyDirective(Directive):
    has_content = True

    def run(self):
        self.assert_has_content()
        node = exception_hierarchy('\n'.join(self.content))
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def setup(app):
    app.add_node(
        exception_hierarchy,
        html=(visit_html_exception_hierarchy_node, depart_html_exception_hierarchy_node),
        latex=(visit_any_exception_hierarchy_node, depart_any_exception_hierarchy_node)
    )
    app.add_directive('exception_hierarchy', ExceptionHierarchyDirective)
