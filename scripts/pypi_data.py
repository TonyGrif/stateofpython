from pypi import PypiIndexClient, PypiJsonClient
from pypi.parsers import parse_classifiers, parse_keywords
import os
from sqlalchemy import ARRAY, MetaData, create_engine, Table, Column, String
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
        Column("documentation_url", String),
        Column("latest_version", String),
        Column("summary", String),
        Column("development_status", String),
        Column("environment", ARRAY(String)),
        Column("intended_audience", ARRAY(String)),
        Column("license", ARRAY(String)),
        Column("operating_system", ARRAY(String)),
        Column("programming_language", ARRAY(String)),
        Column("topic", ARRAY(String)),
        Column("keywords", ARRAY(String)),
    )

    metadata.create_all(engine, checkfirst=True)

    with PypiIndexClient() as client:
        project_index = client.list_projects()

    # Assortment of popular projects to test functionality before running whole set
    testing_repos = [
        "requests",
        "httpx",
        "tensorflow",
        "scikit-learn",
        "pandas",
        "polars",
        "numpy",
        "uv",
        "poetry",
        "rich",
        "click",
        "pytest",
        "ruff",
        "black",
        "mypy",
        "ty",
    ]

    with PypiJsonClient() as client, engine.connect() as connection:
        for count, project in enumerate(project_index):
            if project not in testing_repos:
                continue

            # TODO: Log all this
            try:
                pypidata = client.project_info(project).get("info", {})
            except Exception:
                continue

            data = {}

            if (urls := pypidata.get("project_urls")) is not None:
                urls = {k.lower(): v for k, v in urls.items()}
                data["github_url"] = urls.get("source")
                if data["github_url"] is None:
                    data["github_url"] = urls.get("repository")

                data["homepage_url"] = urls.get("homepage")
                data["documentation_url"] = urls.get("documentation")

            data = data | {
                "repository": project,
                "latest_version": pypidata.get("version"),
                "summary": pypidata.get("summary"),
            }

            data["keywords"] = parse_keywords(pypidata.get("keywords"))

            classifiers = parse_classifiers(pypidata.get("classifiers", []))
            data = data | classifiers

            connection.execute(insert(table), data)
            connection.commit()

            # if count > 200:
            #     break


if __name__ == "__main__":
    main()
