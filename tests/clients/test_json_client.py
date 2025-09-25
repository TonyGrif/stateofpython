from pypi import PypiJsonClient


class TestJsonClient:
    def test_project_info(self):
        with PypiJsonClient() as client:
            result = client.project_info("pandas")
            assert result != {}

            info = result["info"]
            assert "Topic :: Scientific/Engineering" in info["classifiers"]
            assert (
                info["project_urls"]["repository"]
                == "https://github.com/pandas-dev/pandas"
            )
            assert (
                info["summary"]
                == "Powerful data structures for data analysis, time series, and statistics"
            )

    def test_release_info(self):
        with PypiJsonClient() as client:
            result = client.release_info("billboard", "0.3.4")
            assert result != {}

            info = result["info"]
            assert info["author"] == "TonyGrif"
            assert info["requires_python"] == "<4.0,>=3.9"

    def test_all_versions(self):
        with PypiJsonClient() as client:
            result = client.all_versions("billboard")
            assert result != []

            assert len(result) == 2
            assert "0.3.4" in result

    def test_latest_version(self):
        with PypiJsonClient() as client:
            result = client.latest_version("billboard")
            assert result == "0.4.0"
