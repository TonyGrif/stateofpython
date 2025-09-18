from pypi.index import PypiIndexClient


class TestIndexClient:
    def test_project_list(self):
        with PypiIndexClient() as client:
            result = client.list_projects()
            assert result != []

            assert "pandas" in result
            assert "numpy" in result
            assert "tensorflow" in result

    def test_project_files(self):
        with PypiIndexClient() as client:
            result = client.project_files("pandas")
            assert result != []
