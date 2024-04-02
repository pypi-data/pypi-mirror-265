"""GitHub Client class file."""

import re
import sys


class Client:
    """GitHub Client class."""

    def __init__(self, auth, github, app_project=None):
        """Initialize a class instance."""
        self.auth = auth
        self.github = github

        self.datastore = self.github.datastore(auth)
        self.firestore = self.github.firestore(auth, app_project=app_project)

    def auditlogs_restore(self, args=None):
        """Restore users to repos or teams from audit logs."""
        auditlogs = self.github.auditlogs(auth=self.auth, args=args)
        logs = list(auditlogs.import_logs())
        if not logs:
            return
        auditlogs.display_logs(logs)
        print(f'Your filters matched {len(logs)} audit log entries.')
        if auditlogs.flags.action == 'repo.remove_member':
            resource = 'repo collaborator'
        elif auditlogs.flags.action == 'team.remove_member':
            resource = 'team member'
        else:
            error = f'Unsupported action: {auditlogs.flags.action}'
            sys.exit(error)
        if len(logs) > 1:
            resource += 's'
        response = input(f'\nRestore {len(logs)} {resource} from the log entries above? [y/N]: ')
        if not re.match('(y|Y)', response):
            sys.exit('Exiting.')

        if auditlogs.flags.action == 'repo.remove_member':
            auditlogs.restore_repos_collaborators(logs)
        elif auditlogs.flags.action == 'team.remove_member':
            auditlogs.restore_teams_members(logs)

    def auditlogs_stats(self, args=None):
        """Display stats about the audit logs."""
        auditlogs = self.github.auditlogs(auth=self.auth, args=args)
        logs = auditlogs.import_logs()
        stats = auditlogs.get_stats(logs)
        auditlogs.display_stats(stats)

    def broadies_list(self):
        """List Broad GitHub Users."""
        print('Getting People from Firestore...')
        people = self.firestore.get_people()
        users = []
        for person in sorted(people, key=lambda x: x.get('email_username', '').lower()):
            if not person.get('github_id'):
                continue
            print('{} -> {} [{}]'.format(
                person['email_username'],
                person['github_login'],
                person['github_id'],
            ))
            users.append(person)
        print(f'Total Linked GitHub Users: {len(users)}')

    def collaborators_list(self):
        """List GitHub Collaborators."""
        print('Getting GitHub collaborators...')
        github_collaborators = self.github.get_org_outside_collaborators()
        print(f'Found {len(github_collaborators)} collaborators in organization: {self.github.org}.')
        for c in sorted(github_collaborators, key=lambda x: x['login'].lower()):
            print('{} [{}]'.format(c['login'].lower(), c['id']))

    def invitations_list(self):
        """List GitHub Invitations."""
        print('Getting GitHub invitations...')
        github_invitations = self.github.get_org_invitations()
        print(f'Found {len(github_invitations)} invitations in organization: {self.github.org}.')
        for i in sorted(github_invitations, key=lambda x: x['login'].lower()):
            print('{}: {} ({}) [{}]'.format(
                i['login'].lower(),
                i['created_at'],
                i['role'],
                i['id'],
            ))

    def members_list(self, insecure=False):
        """List GitHub Members."""
        print('Getting GitHub members...')
        github_members = self.github.get_org_members(insecure=insecure)
        print(f'Found {len(github_members)} members in organization: {self.github.org}.')
        for m in sorted(github_members, key=lambda x: x['login'].lower()):
            admin = ''
            if m['site_admin']:
                admin = ' (admin)'
            print('{} [{}]{}'.format(
                m['login'].lower(),
                m['id'],
                admin
            ))

    def organization_audit(self):
        """Audit the github organiztaion."""
        print(f'Organization Name: {self.github.org}')

        print('\nGetting organization members...')
        members = self.github.get_org_members()
        print(f'Found {len(members)} organization members.')

        print('\nGetting organization collaborators...')
        collaborators = self.github.get_org_outside_collaborators()
        print(f'Found {len(collaborators)} organization collaborators.')

        print('\nGetting owner account members...')
        owners = self.github.get_org_members(role='admin')
        for user in sorted(owners, key=lambda x: x['login'].lower()):
            print('   * {} [{}]'.format(user['login'].lower(), user['id']))
        print(f'Found {len(owners)} owner account members.')

        print('\nGetting role account members...')
        role_members = self.github.get_team_members(self.github.role_team)
        for user in sorted(role_members, key=lambda x: x['login'].lower()):
            print('   * {} [{}]'.format(user['login'].lower(), user['id']))
        print(f'Found {len(role_members)} role account members.')

        print('\nGetting open organization invitations...')
        invitations = self.github.get_org_invitations()
        for i in sorted(invitations, key=lambda x: x['login'].lower()):
            print('   * {} [{}]'.format(i['login'].lower(), i['id']))
        print(f'Found {len(invitations)} open organization invitations.')

        print('\nGetting organization repos...')
        repos = self.github.get_org_repos()
        private_repos = []
        public_repos = []
        for r in sorted(repos, key=lambda x: x['name']):
            if r['private']:
                private_repos.append(r)
            else:
                public_repos.append(r)
        print(f'   * private repos: {len(private_repos)}')
        print(f'   * public repos: {len(public_repos)}')
        print(f'Found {len(repos)} organization repos.')

        print('\nGetting organization teams...')
        teams = self.github.get_org_teams()
        print(f'Found {len(teams)} organization teams.')

    def public_members_list(self):
        """List GitHub Public Mmebers."""
        print('Getting GitHub public_members...')
        github_members = self.github.get_org_public_members()
        print(f'Found {len(github_members)} public_members in organization: {self.github.org}.')
        for m in sorted(github_members, key=lambda x: x['login'].lower()):
            print('{} [{}]'.format(m['login'].lower(), m['id']))

    def repo_hooks_list(self):
        """List GitHub Repo Hooks."""
        print('Getting GitHub repos...')
        github_repos = self.github.get_org_repos()
        print(f'Found {len(github_repos)} repos in organization: {self.github.org}.')
        for r in sorted(github_repos, key=lambda x: x['name']):
            hooks = self.github.get_repo_hooks(r['name'])
            if hooks:
                print('{}/{}:'.format(self.github.org, r['name']))
                for h in hooks:
                    # get repo hook name
                    name = h['name']
                    if name == 'web':
                        name = h['config'].get('url')
                    # get repo hook status
                    status = 'inactive'
                    if h['active']:
                        status = 'active'
                    print(f'  - {name}: ({status})')

    def repo_hooks_search(self, query):
        """List GitHub Repo Hooks."""
        print('Getting GitHub repos...')
        github_repos = self.github.get_org_repos()
        print(f'Found {len(github_repos)} repos in organization: {self.github.org}.')
        for r in sorted(github_repos, key=lambda x: x['name']):
            hooks = self.github.get_repo_hooks(r['name'])
            if hooks:
                matches = []
                for h in hooks:
                    name = h['name']
                    if name == 'web':
                        name = h['config'].get('url')
                    h['displayName'] = name
                    # find a match
                    if re.search(query, name):
                        matches.append(h)
                if matches:
                    print('{}/{}:'.format(self.github.org, r['name']))
                for h in matches:
                    status = 'inactive'
                    if h['active']:
                        status = 'active'
                    print('  - {}: ({}) [{}]'.format(
                        h['displayName'],
                        h['config']['content_type'],
                        status,
                    ))

    def repos_list(self):
        """List GitHub Repos."""
        print('Getting GitHub repos...')
        github_repos = self.github.get_org_repos()
        print(f'Found {len(github_repos)} repos in organization: {self.github.org}.')
        for r in sorted(github_repos, key=lambda x: x['name']):
            print('{} [{}]'.format(r['name'], r['id']))

    def role_accounts_list(self):
        """List GitHub Role Accounts."""
        print('Getting GitHub Role Accounts...')
        team = self.github.get_team(self.github.role_team)
        role_accounts = self.github.get_team_members(team['id'])
        for m in sorted(role_accounts, key=lambda x: x['login'].lower()):
            print('{} [{}]'.format(m['login'].lower(), m['id']))

    def services_list(self):
        """List GitHub Services."""
        print('Getting GitHub repos...')
        github_repos = self.github.get_org_repos()
        print(f'Found {len(github_repos)} repos in organization: {self.github.org}.')
        for r in sorted(github_repos, key=lambda x: x['name']):
            hooks = self.github.get_repo_hooks(r['name'])
            if hooks:
                output = ''
                for h in hooks:
                    name = h['name']
                    if name == 'web':
                        continue
                    # get hook status
                    status = 'inactive'
                    if h['active']:
                        status = 'active'
                    # set output
                    output += f'  - {name}: ({status})\n'
                if output:
                    print('{}/{}:'.format(self.github.org, r['name']))
                    print(output)

    def teams_audit(self):  # noqa: PLR0912,PLR0915
        """Audit github teams."""
        print('\nGetting organization teams...')
        teams = self.github.get_org_teams()
        print(f'Found {len(teams)} organization teams.')

        print('\nGetting cached teams members...')
        teams_members = self.firestore.get_teams_members_dict()
        print(f'Found {len(teams_members)} teams members.')

        print('\nGetting cached teams repos...')
        teams_repos = self.firestore.get_teams_repos_dict()
        print(f'Found {len(teams_repos)} teams repos.')

        print('\nGetting org admins...')
        owners = self.github.get_org_members(role="admin")
        print(f'Found {len(owners)} org admins.')

        print('\nGetting team syncs...')
        team_syncs = self.firestore.get_team_syncs_dict()
        print(f'Found {len(team_syncs)} team syncs.')

        print('\nChecking for teams with no members or no repos:')

        nomembers = []
        norepos = []
        onemember = []
        for t in sorted(teams, key=lambda x: x['slug']):
            tid = t['id']
            tmembers = teams_members.get(tid, {})
            trepos = teams_repos.get(tid, {})
            if not tmembers.get('members', []):
                nomembers.append(t)
            if len(tmembers.get('members', [])) == 1:
                onemember.append(t)
            if not trepos.get('repos', []):
                norepos.append(t)

        print(f'Found {len(nomembers)} teams with no members.')
        print(f'Found {len(onemember)} teams with one member.')
        print(f'Found {len(norepos)} teams with no repos.')

        if nomembers:
            print('\nTeams with no members:')
            for team in sorted(nomembers, key=lambda x: x['slug']):
                slug = team['slug']
                team_url = 'https://github.com/orgs/broadinstitute/teams'
                note = ''
                if slug in team_syncs:
                    note = ' - syncing from {}!'.format(
                        team_syncs[slug]['group_email'],
                    )
                print('   * {} [{}]: {}/{}{}'.format(
                    slug,
                    t['id'],
                    team_url,
                    slug,
                    note
                ))

        if onemember:
            print('\nTeams with one member:')
            for team in sorted(onemember, key=lambda x: x['slug']):
                slug = team['slug']
                team_url = 'https://github.com/orgs/broadinstitute/teams'
                note = ''
                if slug in team_syncs:
                    note = ' - syncing from {}!'.format(
                        team_syncs[slug]['group_email'],
                    )
                print('   * {} [{}]: {}/{}{}'.format(
                    slug,
                    t['id'],
                    team_url,
                    slug,
                    note
                ))

        if norepos:
            print('\nTeams with no repos:')
            for team in sorted(norepos, key=lambda x: x['slug']):
                slug = team['slug']
                team_url = 'https://github.com/orgs/broadinstitute/teams'
                note = ''
                if slug in team_syncs:
                    note = ' - syncing from {}!'.format(
                        team_syncs[slug]['group_email'],
                    )
                print('   * {} [{}]: {}/{}{}'.format(
                    slug,
                    t['id'],
                    team_url,
                    slug,
                    note
                ))

        print(f'\nTeams with Google Group Syncs [{len(team_syncs)}]:')
        for slug in sorted(team_syncs):
            sync = team_syncs[slug]
            tid = sync['team_id']

            maintainers = self.github.get_team_members(tid, role='maintainer')
            logins = []
            for user in maintainers:
                uid = user['id']
                if uid in owners:
                    continue
                login = user['login']
                logins.append(login)

            print('   * {} <-- {}: {}'.format(
                slug,
                sync['group_email'],
                ', '.join(sorted(logins))
            ))

        nomaintainer = []

        print(f'\nTeams without Google Group Syncs [{len(teams) - len(team_syncs)}]:')

        print('\n  With a Maintainer:')
        for team in sorted(teams, key=lambda x: x['slug']):
            tid = team['id']
            slug = team['slug']
            if slug in team_syncs:
                continue

            maintainers = self.github.get_team_members(tid, role='maintainer')
            logins = []
            for user in maintainers:
                login = user['login']
                logins.append(login)

            if not logins:
                nomaintainer.append(team)
                continue

            print('     * {} [{}]: {}'.format(
                slug,
                tid,
                ', '.join(sorted(logins)),
            ))

        print('\n  Without a Maintainer:')
        for team in sorted(nomaintainer, key=lambda x: x['slug']):
            slug = team['slug']
            print('     * {} [{}]'.format(slug, team['id']))

    def team_syncs_list(self):
        """List GitHub Team Syncs."""
        print('Getting GitHub team syncs...')
        team_syncs = self.firestore.get_team_syncs_dict()
        print(f'Found {len(team_syncs)} syncs.')
        for oid in sorted(team_syncs, key=lambda x: team_syncs[x]['google_group']):
            s = team_syncs[oid]
            print('{} --> {} [{}]'.format(
                s['google_group'],
                s['github_team_slug'],
                s['github_team']
            ))

    def teams_list(self):
        """List Github teams."""
        print('Getting GitHub teams...')
        teams = self.github.get_org_teams()
        print(f'Found {len(teams)} teams in organization: {self.github.org}.')
        for r in sorted(teams, key=lambda x: x['slug']):
            print('{} [{}]'.format(r['slug'], r['id']))
