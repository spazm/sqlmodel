import uuid
from typing import Annotated, Iterator, Optional

import sqlalchemy.types
from sqlalchemy import func
from sqlalchemy.orm import mapped_column
from sqlmodel import SQLModel, Field, String
import sqlmodel

# from datetime import datetime
# from decimal import Decimal


# from sqlalchemy.dialects import postgresql


uuid_server_pk = Annotated[
    uuid.UUID,
    mapped_column(primary_key=True, server_default=func.gen_random_uuid()),
]
uuid_server = Annotated[uuid.UUID, mapped_column(server_default=func.gen_random_uuid())]

str_20 = Annotated[str, mapped_column(String(20))]  # varchar(20)


def test_annotated_uuid(clear_sqlmodel: Iterator[None]) -> None:
    class Test_Table(SQLModel, table=True):
        id: uuid_server_pk = Field()
        server_uuid: uuid_server
        optional_uuid: Optional[uuid_server]
        unannotated_uuid: uuid.UUID
        first_string: str_20
        second_string: str_20 = Field(max_length=33)

    test_table = Test_Table.metadata.tables["test_table"]

    assert len(test_table.columns) == 6

    columns = list(test_table.columns)


    col = columns.pop(0)
    assert col.name == "id"
    assert isinstance(col.type, sqlalchemy.types.Uuid)
    assert col.primary_key
    assert not col.nullable
    assert col.server_default is not None
    assert isinstance(col.server_default.arg, sqlalchemy.sql.functions.Function)
    assert str(col.server_default.arg) == 'gen_random_uuid()'

    col = columns.pop(0)
    assert col.name == "server_uuid"
    assert isinstance(
        col.type, sqlalchemy.types.Uuid
    )  # sqlalchemy.types.UUID()
    assert not col.primary_key
    assert not col.nullable

    col = columns.pop(0)
    assert col.name == "optional_uuid"
    assert isinstance(col.type, sqlalchemy.types.Uuid)
    assert not col.primary_key
    assert col.nullable

    col = columns.pop(0)
    assert col.name == "unannotated_uuid"
    assert isinstance(col.type, sqlalchemy.types.Uuid)
    assert str(col.type) == 'CHAR(32)'
    assert not col.primary_key
    assert not col.nullable

    col = columns.pop(0)
    assert col.name == 'first_string'
    #assert isinstance(col.type, sqlalchemy.types.String)
    assert str(col.type) == 'VARCHAR(20)'
    assert col.type.length == 20

    col = columns.pop(0)
    assert col.name == 'second_string'
    #assert isinstance(col.type, sqlmodel.sql.sqltypes.AutoString)
    assert str(col.type) == 'VARCHAR(33)'
    #assert isinstance(col.type, sqlalchemy.types.String)
    assert col.type.length == 33


"""
uuid_server_pk = Annotated[
    uuid.UUID,
    mapped_column(primary_key=True, server_default=func.gen_random_uuid()),
]

timestamp_now = Annotated[
    datetime,
    mapped_column(
        sqlalchemy.types.TIMESTAMP(timezone=True),
        server_default=func.now(),
    ),
]
timestampz = Annotated[
    datetime,
    mapped_column(
        sqlalchemy.types.TIMESTAMP(timezone=True),
    ),
]
timestampz_now = Annotated[
    datetime,
    mapped_column(
        # sqlalchemy.types.TIMESTAMP(timezone=True),
        postgresql.TIMESTAMP(timezone=True, precision=0),
        server_default=func.now(),
    ),
]
timestampz_now_fetch = Annotated[
    datetime,
    mapped_column(
        sqlalchemy.types.TIMESTAMP(timezone=True),
        server_default=func.now(),
        server_onupdate=FetchedValue(),  # fetch updated value via returning on row updates
    ),
]

str_20 = Annotated[Optional[str], mapped_column(String(20))]


class Fake(SQLModel, table=True):
    # id: uuid_server_pk = Field(max_length=22,
    #                           #sa_column_args=['foo_id']
    #                           )
    id: int = Field(
        # max_length=30,
        # primary_key=True,
        sa_column=mapped_column(
            "def",
            Integer,
            # name="abc",
            autoincrement=True,  # "auto",
            primary_key=True,
        ),
        # sa_column_kwargs={
        #    ##"server_default": "def",
        #    #"name": "abc",
        #    "autoincrement": True,  # "auto",
        #    "primary_key": True,
        # },
        default="abc",
    )
    fake_timestamp_now: timestamp_now
    fake_timestampz_now: timestampz_now
    fake_timestampz_now_fetch: timestampz_now_fetch
    uuid_test_1: uuid_server_pk
    foo: str = Field(max_length=33)
    bar_20: str_20 = Field()
    bar_25: str_20 = Field(max_length=25)
    baz_dec: Decimal = Field(sa_type=sqlalchemy.types.DECIMAL)
    bar_dec: Decimal = Field(max_digits=3, decimal_places=5)


if __name__ == "__main__":
    metadata = Fake.metadata
    tables = metadata.tables.keys()
    for table in tables:
        print(f"table: {table}")

        create_table = CreateTable(metadata.tables[table]).compile(
            dialect=postgresql.dialect()
        )
        print(str(create_table))
"""
