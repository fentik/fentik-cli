import json
import sys
from pathlib import Path


class StatusCommand:
    def __init__(self, client):
        self._client = client

    def _file_contents(self, path):
        with open(path, 'r') as f:
            return f.read()

    def _status(self, args):
        res = self._client.query(
            """
                query GetDevDeployStatus {
                  devDeployStatus {
                    totalModels
                    totalSources,
		            numSourcesDeployed,
                    numModelsDeployed,
                    startedAt,
                    endedAt,
                }
        }
        """
        )
        json_res = json.loads(res)
        result = json_res["data"]["devDeployStatus"]
        if result['totalModels'] == 0:
            print("No models deployed in your sandbox. Use fentik deploy <model>.")
        else:
            print(f"Deployed {result['numModelsDeployed']} out of {result['totalModels']}")

    def register_subparser(self, subparsers):
        parser = subparsers.add_parser('status', help="Get the status of dev")
        parser.set_defaults(func=self._status)
