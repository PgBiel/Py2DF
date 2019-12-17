"""A directive for indicating that a rank is required."""
import sphinx
from docutils import nodes
from docutils.parsers.rst.directives.admonitions import BaseAdmonition

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective


sphinx.locale.admonitionlabels['rank'] = 'Minimum Rank Required'


class rank(nodes.Admonition, nodes.Element):
    pass


def visit_rank_node(self, node):
    try:
        self.visit_admonition(node, "rank")
    except TypeError:
        self.visit_admonition(node)


def depart_rank_node(self, node):
    self.depart_admonition(node)


class RankDirective(BaseAdmonition):
    """Rank directive.

    Usage::

        .. rank:: overlord/mythic/emperor/noble
    """
    node_class = rank

    # # this enables content in the directive
    # has_content = True
    # required_arguments = 1
    #
    # def run(self):
    #     targetid = 'rank-%d' % self.env.new_serialno('rank')
    #     targetnode = nodes.target('', '', ids=[targetid])
    #
    #     rank_node = rank(self.arguments[0].capitalize())
    #     # rank_node += nodes.title(_('Minimum Rank Required'), _('Minimum Rank Required:'))
    #     self.state.nested_parse([self.arguments[0].capitalize()], self.content_offset, rank_node)
    #
    #     if not hasattr(self.env, 'rank_all_ranks'):
    #         self.env.rank_all_ranks = []
    #
    #     self.env.rank_all_ranks.append({
    #         'docname': self.env.docname,
    #         'lineno': self.lineno,
    #         'rank': rank_node.deepcopy(),
    #         'target': targetnode,
    #     })
    #
    #     return [targetnode, rank_node]


# def purge_ranks(app, env, docname):
#     if not hasattr(env, 'rank_all_ranks'):
#         return
#
#     env.rank_all_ranks = [rank for rank in env.rank_all_ranks
#                           if rank['docname'] != docname]


def setup(app):
    app.add_node(rank,
                 html=(visit_rank_node, depart_rank_node),
                 latex=(visit_rank_node, depart_rank_node),
                 text=(visit_rank_node, depart_rank_node))

    app.add_directive('rank', RankDirective)
    # app.connect('env-purge-doc', purge_ranks)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
