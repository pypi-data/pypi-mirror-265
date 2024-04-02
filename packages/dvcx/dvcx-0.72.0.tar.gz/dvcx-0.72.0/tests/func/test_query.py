import json
from textwrap import dedent

import dill
import pytest

from dvcx.catalog import QUERY_DATASET_NAME_PREFIX
from dvcx.cli import query
from dvcx.query import C, DatasetQuery


@pytest.fixture
def catalog_info_filepath(cloud_test_catalog_tmpfile, tmp_path):
    catalog = cloud_test_catalog_tmpfile.catalog

    catalog_info = {
        "catalog_init_params": catalog.get_init_params(),
        "id_generator_params": catalog.id_generator.clone_params(),
        "metastore_params": catalog.metastore.clone_params(),
        "warehouse_params": catalog.warehouse.clone_params(),
    }
    catalog_info_filepath = tmp_path / "catalog-info"
    with open(catalog_info_filepath, "wb") as f:
        dill.dump(catalog_info, f)

    return catalog_info_filepath


def setup_catalog(query: str, catalog_info_filepath: str) -> str:
    query_catalog_setup = f"""\
    import dill
    from dvcx.catalog import Catalog

    catalog_info_filepath = {str(catalog_info_filepath)!r}
    with open(catalog_info_filepath, "rb") as f:
        catalog_info = dill.load(f)
    (
        id_generator_class,
        id_generator_args,
        id_generator_kwargs,
    ) = catalog_info["id_generator_params"]
    id_generator = id_generator_class(*id_generator_args, **id_generator_kwargs)
    (
        metastore_class,
        metastore_args,
        metastore_kwargs,
    ) = catalog_info["metastore_params"]
    metastore = metastore_class(*metastore_args, **metastore_kwargs)
    (
        warehouse_class,
        warehouse_args,
        warehouse_kwargs,
    ) = catalog_info["warehouse_params"]
    warehouse = warehouse_class(*warehouse_args, **warehouse_kwargs)
    catalog = Catalog(
        id_generator=id_generator,
        metastore=metastore,
        warehouse=warehouse,
        **catalog_info["catalog_init_params"],
    )
    """
    return dedent(query_catalog_setup + "\n" + query)


def test_query_cli(cloud_test_catalog_tmpfile, tmp_path, catalog_info_filepath, capsys):
    catalog = cloud_test_catalog_tmpfile.catalog
    src_uri = cloud_test_catalog_tmpfile.src_uri

    query_script = f"""\
    from dvcx.query import C, DatasetQuery

    DatasetQuery({src_uri!r}, catalog=catalog)
    """
    query_script = setup_catalog(query_script, catalog_info_filepath)

    filepath = tmp_path / "query_script.py"
    filepath.write_text(query_script)

    ds_name = "my-dataset"
    query(catalog, str(filepath), ds_name)
    captured = capsys.readouterr()
    assert captured.err == ""
    printed_rows = captured.out.strip().split("\n")[-7:]
    rows = [json.loads(r) for r in printed_rows]
    rows = sorted(rows, key=lambda r: r["name"])
    assert [r["name"] for r in rows] == [
        "cat1",
        "cat2",
        "description",
        "dog1",
        "dog2",
        "dog3",
        "dog4",
    ]

    result = (
        DatasetQuery(src_uri, catalog=catalog)
        .select(C.source, C.parent, C.name, C.vtype, C.size)
        .order_by(C.source, C.parent, C.name)
        .to_records()
    )

    assert result == [
        {
            "source": src_uri,
            "parent": "",
            "name": "description",
            "vtype": "",
            "size": 13,
        },
        {
            "source": src_uri,
            "parent": "cats",
            "name": "cat1",
            "vtype": "",
            "size": 4,
        },
        {
            "source": src_uri,
            "parent": "cats",
            "name": "cat2",
            "vtype": "",
            "size": 4,
        },
        {
            "source": src_uri,
            "parent": "dogs",
            "name": "dog1",
            "vtype": "",
            "size": 4,
        },
        {
            "source": src_uri,
            "parent": "dogs",
            "name": "dog2",
            "vtype": "",
            "size": 3,
        },
        {
            "source": src_uri,
            "parent": "dogs",
            "name": "dog3",
            "vtype": "",
            "size": 4,
        },
        {
            "source": src_uri,
            "parent": "dogs/others",
            "name": "dog4",
            "vtype": "",
            "size": 4,
        },
    ]


def test_query(cloud_test_catalog_tmpfile, tmp_path, catalog_info_filepath):
    catalog = cloud_test_catalog_tmpfile.catalog
    src_uri = cloud_test_catalog_tmpfile.src_uri

    query_script = f"""\
    from dvcx.query import C, DatasetQuery

    DatasetQuery({src_uri!r}, catalog=catalog)
    """
    query_script = setup_catalog(query_script, catalog_info_filepath)

    dataset, version, output = catalog.query(query_script, save=True)
    assert dataset.name.startswith(QUERY_DATASET_NAME_PREFIX)
    assert dataset.query_script == query_script
    assert version == 1
    assert dataset.versions_values == [1]
    assert {r.name for r in catalog.ls_dataset_rows(dataset.name, version)} == {
        "cat1",
        "cat2",
        "description",
        "dog1",
        "dog2",
        "dog3",
        "dog4",
    }


def test_query_where_last_command_is_call_on_save_which_returns_attached_dataset(
    cloud_test_catalog_tmpfile, tmp_path, catalog_info_filepath
):
    """
    Testing use case where last command is call on DatasetQuery save which returns
    attached instance to underlying saved dataset
    """
    catalog = cloud_test_catalog_tmpfile.catalog
    src_uri = cloud_test_catalog_tmpfile.src_uri

    query_script = f"""\
    from dvcx.query import C, DatasetQuery

    DatasetQuery({src_uri!r}, catalog=catalog).filter(C.name.glob("dog*")).save("dogs")
    """
    query_script = setup_catalog(query_script, catalog_info_filepath)

    dataset, version, output = catalog.query(query_script, save=True)
    assert not dataset.name.startswith(QUERY_DATASET_NAME_PREFIX)
    assert dataset.query_script == query_script
    assert version == 1
    assert dataset.versions_values == [1]
    assert {r.name for r in catalog.ls_dataset_rows(dataset.name, version)} == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
    }


def test_query_where_last_command_is_attached_dataset_query_created_from_save(
    cloud_test_catalog_tmpfile, tmp_path, catalog_info_filepath
):
    """
    Testing use case where last command is instance of DatasetQuery which is
    attached to underlying dataset by calling save just before
    """
    catalog = cloud_test_catalog_tmpfile.catalog
    src_uri = cloud_test_catalog_tmpfile.src_uri

    query_script = f"""\
    from dvcx.query import C, DatasetQuery

    ds = DatasetQuery(
        {src_uri!r}, catalog=catalog
    ).filter(C.name.glob("dog*")).save("dogs")
    ds
    """
    query_script = setup_catalog(query_script, catalog_info_filepath)

    dataset, version, output = catalog.query(query_script, save=True)
    assert dataset.name == "dogs"
    assert dataset.query_script == query_script
    assert version == 1
    assert dataset.versions_values == [1]
    assert {r.name for r in catalog.ls_dataset_rows(dataset.name, version)} == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
    }


def test_query_where_last_command_is_attached_dataset_query_created_from_query(
    cloud_test_catalog_tmpfile, tmp_path, catalog_info_filepath
):
    """
    Testing use case where last command is instance of DatasetQuery which is
    attached to underlying dataset by creating query pointing to it
    """
    catalog = cloud_test_catalog_tmpfile.catalog
    src_uri = cloud_test_catalog_tmpfile.src_uri

    query_script = f"""\
    from dvcx.query import C, DatasetQuery

    ds = DatasetQuery(
        {src_uri!r}, catalog=catalog
    ).filter(C.name.glob("dog*")).save("dogs")
    DatasetQuery(name="dogs", version=1)
    """
    query_script = setup_catalog(query_script, catalog_info_filepath)

    dataset, version, output = catalog.query(query_script, save=True)
    assert dataset.name == "dogs"
    assert dataset.query_script == query_script
    assert version == 1
    assert dataset.versions_values == [1]
    assert {r.name for r in catalog.ls_dataset_rows(dataset.name, version)} == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
    }
