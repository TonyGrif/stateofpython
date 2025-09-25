from pypi import PypiIndexClient, PypiJsonClient
import os
from sqlalchemy import MetaData, create_engine, Table, Column, String
from sqlalchemy.sql import insert


def main() -> None:
    constr = os.environ["SQL_ALCHEMY_CONN"]
    engine = create_engine(constr)

    metadata = MetaData()
    table = Table(
        "PyPi",
        metadata,
        Column("repository", String, primary_key=True),
        Column("github_url", String),
        Column("homepage_url", String),
        Column("latest_version", String),
        Column("summary", String),
    )

    metadata.create_all(engine, checkfirst=True)

    with PypiIndexClient() as client:
        project_index = client.list_projects()

    with PypiJsonClient() as client, engine.connect() as connection:
        for count, project in enumerate(project_index):
            # TODO: Log all this
            try:
                pypidata = client.project_info(project).get("info", {})
            except Exception:
                continue

            data = {}

            if (urls := pypidata.get("project_urls")) is not None:
                data["github_url"] = urls.get("source")
                data["homepage_url"] = urls.get("homepage")

            data = data | {
                "repository": project,
                "latest_version": pypidata.get("version"),
                "summary": pypidata.get("summary"),
            }

            connection.execute(insert(table), data)
            connection.commit()


if __name__ == "__main__":
    main()
