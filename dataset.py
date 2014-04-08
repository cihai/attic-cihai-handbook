# -*- coding: utf-8 -*-
"""
    _extensions.dataset
    ~~~~~~~~~~~~~~~~~~~

    What can we do with this.

    Create a

    .. grid:: namespace
        :pkColumnName:  hi
        :columns: hi,hi, (find syntax for list of items in options) or collect
            all grid items for that grid

    .. grid-item:: primaryName
        :namespace: myGrid

    :copyright: (c) 2013 by Tony Narlock.
    :license: BSD, see LICENSE for more details.
"""

# from __future__ import absolute_import, division, print_function, \
    # with_statement, unicode_literals

from sphinx.util.compat import Directive
from docutils.parsers.rst import directives
from docutils import nodes, utils
from docutils.parsers.rst.roles import set_classes

from pprint import pprint

import os

gh_repo_tpl = """\
{name} watch {watchers} forks {forks}
"""

gh_pr_tpl = """\
+{{additions}} -{{deletions}} {{created_at}}
"""


class GitHubRepoDirective(Directive):
    """Directive for Github Repositories."""
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = False
    option_spec = {
        "travis": directives.uri,
        "docs": directives.uri,
        "api": directives.uri,
        "pypi": directives.uri,
        "homepage": directives.uri,
        "use_gh_description": directives.flag,
    }

    def run(self):
        repo = self.arguments[0]
        env = self.state.document.settings.env

        try:
            repo_user, repo_name = repo.split('/')
            repo = gh.repository(repo_user, repo_name)
        except Exception as e:
            raise self.error("GitHub API error: %s" % e.message)

        tpl = gh_repo_tpl
        html = tpl.format(**repo.__dict__)

        if not hasattr(env, 'github_repo_all_repos'):
            env.github_repo_all_repos = []
            env.github_repo_all_repos.append({
                'docname': env.docname,
                'lineno': self.lineno,
                'repo': repo,
            })

        repo_link = nodes.reference('', 'github', refuri=repo.html_url)

        title = nodes.paragraph()
        title += repo_link,
        if 'travis' in self.options:
            title += nodes.inline('', ' - ')
            title += nodes.reference(
                '', 'travis', refuri=self.options.get('travis'))

        if 'docs' in self.options:
            title += nodes.inline('', ' - ')
            title += nodes.reference(
                '', 'docs', refuri=self.options.get('docs'))

        if 'api' in self.options:
            title += nodes.inline('', ' - ')
            title += nodes.reference(
                '', 'api', refuri=self.options.get('api'))

        if 'pypi' in self.options:
            title += nodes.inline('', ' - ')
            title += nodes.reference(
                '', 'pypi', refuri=self.options.get('pypi'))

        if 'homepage' in self.options:
            title += nodes.inline('', ' - ')
            title += nodes.reference(
                '', 'homepage', refuri=self.options.get('homepage'))

        if repo.watchers > 10:
            title += nodes.inline('', ' - %s watchers' % str(repo.watchers))

        if repo.forks > 10:
            title += nodes.inline('', ' -  %s forks' % str(repo.forks))

        new_nodes = [title]

        if 'use_gh_description' in self.options:
            new_nodes.append(nodes.paragraph('', repo.description))

        return new_nodes


def purge_repos(app, env, docname):
    if not hasattr(env, 'github_repo_all_repos'):
        return

    env.github_repo_all_repos = [
        repo for repo in env.github_repo_all_repos if repo['docname'] != docname
    ]


def github_repo_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """github repo role."""
    try:
        repo_user, repo_name = text.split('/')
        repo = gh.repository(repo_user, repo_name)
    except Exception as e:
        msg = inliner.reporter.error(
            'GitHub API error: %s for "%s"' % e.message, text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    tpl = gh_repo_tpl
    html = tpl.format(**repo.__dict__)

    title = nodes.paragraph()
    title += nodes.inline('', repo_name + ': ')
    title += nodes.reference('', 'github', refuri=repo.html_url)

    return [title], []


def github_pr_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Here are some docs.

    :param rawtext: Text being replaced with link node.
    :param app: Sphinx application context
    :param type: Link type (issue, changeset, etc.)
    :param slug: ID of the thing to link to
    :param options: Options dictionary passed to role func.
    """

    try:
        pr = text
        if not pr or len(pr) <= 0 or not isinstance(text, basestring):
            raise ValueError
    except ValueError:
        msg = inliner.reporter.error(
            'pull request should be in the format of /:user/:repo/pull/:pull_id'
            '"%s" is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    set_classes(options)

    repo_user, repo_name, pull, pull_id = pr.split('/')

    repo = gh.repository(repo_user, repo_name)
    pull = repo.pull_request(pull_id)

    tpl = gh_pr_tpl
    attributes = pull.__dict__
    attributes['repo_name'] = pull.repository[1]
    pr_details = gh_pr_tpl.format(attributes)

    # <a href={{repo.html_url}}>repo_name</a>
    repo_link = nodes.reference(
        rawtext, repo_name, refuri=repo.html_url, **options)
    # <em>pull.title</em>
    pr_title_emphasized = nodes.emphasis(rawtext, pull.title, **options)
    # ./tpl/gh_pr.rst
    pr_details_node = nodes.emphasis(rawtext, pr_details, **options)
    pr_number_link = nodes.reference(rawtext, '#' + str(
        pull.number), refuri=pull.html_url, **options)
    pr_additions = nodes.inline(rawtext, str(pull.additions) + ' additions(+)')
    pr_deletions = nodes.inline(rawtext, str(pull.deletions) + ' deletions(-)')
    pr_created_at = nodes.inline(rawtext, pull.created_at.strftime('%Y-%m-%d'))

    title = nodes.paragraph()
    title += repo_link,
    title += nodes.inline(rawtext, ' ')
    title += nodes.inline(rawtext, ' (')
    title += pr_number_link
    title += nodes.inline(rawtext, ') ')
    title += nodes.inline(rawtext, ' '),
    title += pr_title_emphasized,

    details = nodes.paragraph()
    details += pr_additions
    details += nodes.inline(rawtext, ', ')
    details += pr_deletions
    details += nodes.inline(rawtext, ' '),
    details += pr_created_at

    return [title, details], []


def visit_github_pr_node(self, node):
    pass


def depart_github_pr_node(self, node):
    pass


def setup(app):
    app.add_directive('github-repo', GitHubRepoDirective)
    app.add_role('github-repo', github_repo_role)
    app.add_role('github-pr', github_pr_role)
    app.connect('env-purge-doc', purge_repos)
    print('wat0')
