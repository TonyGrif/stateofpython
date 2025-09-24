from pypi.index import PypiIndexClient
import os
from sqlalchemy import MetaData, create_engine, Table, Column, String
from sqlalchemy.sql import insert


def main() -> None:
    constr = os.environ["SQL_ALCHEMY_CONN"]
    engine = create_engine(constr)

    metadata = MetaData()
    table = Table("PyPi", metadata, Column("repository", String, primary_key=True))

    metadata.create_all(engine, checkfirst=True)

    with PypiIndexClient() as client, engine.connect() as connection:
        result = client.list_projects()
        data = []
        for line in result:
            data.append({"repository": line})

        connection.execute(insert(table), data)
        connection.commit()


if __name__ == "__main__":
    main()
