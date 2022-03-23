import getpass
import os
import sys

from graphqlclient import GraphQLClient


class InitCommand:
    INITAL_DIRS = ['models', 'tests']

    def _init_project(self, args):
        print('Initializing local development enviroment')
        print('creating...')

        for d in self.INITAL_DIRS:
            try:
                if not os.path.exists(d):
                    os.mkdir(d)
                    print(f"\t{d}/")
                else:
                    print(f"\t{d}/ exists, skipping")
            except Exception as e:
                print(f'error creating {d}: ' + e.__str__())
                sys.exit(1)

        # Create the configuration file if needed, which also marks this directory as a project.
        try:
            with open('fentik-config.yml', 'a'):
                pass
        except Exception as e:
            print('error creating fentik-config.yml: ' + e.__str__())
            sys.exit(1)

    def register_subparser(self, subparsers):
        parser = subparsers.add_parser(
            'init', help="Initialize your development environment."
        )
        parser.set_defaults(func=self._init_project)


class FentikClient:
    API_SERVER = os.getenv('FENTIK_API_SERVER', "api.fentik.com")
    BASE_URI = f"https://{API_SERVER}/api/graphql"
    _client = None

    def __init__(self, auth_manager):
        self._auth_manager = auth_manager

    def query(self, query):
        if not self._client:
            # delay initialization until first query in case we don't have
            # a token initialized yet
            self._client = GraphQLClient(self.BASE_URI)
            self._client.inject_token('Token ' + self._auth_manager.get_token())

        return self._client.execute(query)
