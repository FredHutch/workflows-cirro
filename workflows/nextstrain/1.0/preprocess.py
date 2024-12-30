#!/usr/bin/env python3

import boto3
import json
import os
from cirro.helpers.preprocess_dataset import PreprocessDataset


def mock_exclude(ds: PreprocessDataset):
    """Make an empty 'exclude' file"""

    with open("exclude.txt", "w") as _:
        pass
    ds.add_param("exclude", "exclude.txt")


def mock_colors(ds: PreprocessDataset):
    """Provide a default colors file"""

    # If there wasn't a 'colors' file provided
    if ds.params.get("colors") is None:
        ds.logger.info("Using default colors from the zika tutorial")
        ds.add_param(
            "colors",
            "https://raw.githubusercontent.com/nextstrain/zika/main/config/colors.tsv" # noqa
        )


def mock_config(ds: PreprocessDataset):
    """Construct the auspice configuration file"""

    config = {
        "title": ds.params["title"],
        "maintainers": [
            {
                "name": "Trevor Bedford",
                "url": "http://bedford.io/team/trevor-bedford/"
            }
        ],
        "build_url": "https://github.com/nextstrain/zika",
        "colorings": [
            {
                "key": "gt",
                "title": "genotype",
                "type": "categorical"
            },
            {
                "key": "num_date",
                "title": "date",
                "type": "continuous"
            },
            {
                "key": "author",
                "title": "author",
                "type": "categorical"
            },
            {
                "key": "country",
                "title": "country",
                "type": "categorical"
            },
            {
                "key": "region",
                "title": "region",
                "type": "categorical"
            }
        ],
        "geo_resolutions": [
            "country",
            "region"
        ],
        "display_defaults": {
            "map_triplicate": True
        },
        "filters": [
            "country",
            "region",
            "author"
        ]
    }

    ds.logger.info("Auspice Configuration:")
    ds.logger.info(json.dumps(config, indent=4))

    with open("auspice_config.json", "w") as handle:
        json.dump(config, handle, indent=4)

    ds.add_param("auspice_config", "auspice_config.json")
    ds.remove_param("title")


def mock_creds(ds: PreprocessDataset):
    """
    Supply deployment credentials to the workflow,
    if they have been set up in secrets.
    """

    secret_manager = SecretManager(
        os.getenv('PW_SECRETS_NAMESPACE'),
        boto3.client(
            'secretsmanager',
            region_name=os.getenv("PW_AWS_REGION")
        )
    )

    for secret_name in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]:

        if secret_manager.exists(secret_name):

            ds.logger.info(f"Adding {secret_name} to params")
            ds.add_param(
                secret_name.lower(),
                secret_manager.get_value(secret_name),
                log=False
            )


class SecretManager:
    def __init__(self, secret_prefix, client):
        assert secret_prefix is not None, "Must provide $PW_SECRETS_NAMESPACE"
        self.secret_prefix = secret_prefix
        self.client = client

    def exists(self, secret_name):
        try:
            self.client.describe_secret(
                SecretId=f'{self.secret_prefix}/{secret_name}'
            )
            return True
        except Exception:
            return False

    def get_value(self, secret_name):
        resp = self.client.get_secret_value(
            SecretId=f'{self.secret_prefix}/{secret_name}'
        )
        return resp["SecretString"]


if __name__ == "__main__":

    ds = PreprocessDataset.from_running()

    mock_exclude(ds)
    mock_colors(ds)
    mock_config(ds)

    # log
    ds.logger.info(ds.params)

    # Do not log the credentials
    mock_creds(ds)
