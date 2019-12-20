"""A directive for indicating that a workswith is required."""
import sphinx
from docutils import nodes
from docutils.parsers.rst.directives.admonitions import BaseAdmonition

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective


sphinx.locale.admonitionlabels['workswith'] = 'Works With'


class workswith(nodes.Admonition, nodes.Element):
    pass


def visit_workswith_node(self, node):
    try:
        self.visit_admonition(node, "workswith")
    except TypeError:
        self.visit_admonition(node)


def depart_workswith_node(self, node):
    self.depart_admonition(node)


class RankDirective(BaseAdmonition):
    """Rank directive.

    Usage::

        .. workswith:: overlord/mythic/emperor/noble
    """
    node_class = workswith

    # # this enables content in the directive
    # has_content = True
    # required_arguments = 1
    #
    # def run(self):
    #     targetid = 'workswith-%d' % self.env.new_serialno('workswith')
    #     targetnode = nodes.target('', '', ids=[targetid])
    #
    #     workswith_node = workswith(self.arguments[0].capitalize())
    #     # workswith_node += nodes.title(_('Minimum Rank Required'), _('Minimum Rank Required:'))
    #     self.state.nested_parse([self.arguments[0].capitalize()], self.content_offset, workswith_node)
    #
    #     if not hasattr(self.env, 'workswith_all_workswiths'):
    #         self.env.workswith_all_workswiths = []
    #
    #     self.env.workswith_all_workswiths.append({
    #         'docname': self.env.docname,
    #         'lineno': self.lineno,
    #         'workswith': workswith_node.deepcopy(),
    #         'target': targetnode,
    #     })
    #
    #     return [targetnode, workswith_node]


# def purge_workswiths(app, env, docname):
#     if not hasattr(env, 'workswith_all_workswiths'):
#         return
#
#     env.workswith_all_workswiths = [workswith for workswith in env.workswith_all_workswiths
#                           if workswith['docname'] != docname]


def setup(app):
    app.add_node(workswith,
                 html=(visit_workswith_node, depart_workswith_node),
                 latex=(visit_workswith_node, depart_workswith_node),
                 text=(visit_workswith_node, depart_workswith_node))

    app.add_directive('workswith', RankDirective)
    # app.connect('env-purge-doc', purge_workswiths)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
