from pypi.parsers import parse_classifiers, parse_keywords


class TestParsers:
    def test_classifiers(self):
        pd_data = [
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Environment :: GPU :: NVIDIA CUDA :: 12",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Cython",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Scientific/Engineering",
        ]
        result = parse_classifiers(pd_data)

        assert result["development_status"] == ["5 - Production/Stable"]
        assert result["environment"] == ["Console", "GPU :: NVIDIA CUDA :: 12"]
        assert result["intended_audience"] == ["Science/Research"]
        assert result["license"] == ["BSD License"]
        assert result["operating_system"] == ["OS Independent"]
        assert result["topic"] == ["Scientific/Engineering"]

    def test_keywords(self):
        test_data = "automation, formatter, keys"
        result = parse_keywords(test_data)

        assert len(result) == 3
        assert "formatter" in result

        null_data = ""
        result = parse_keywords(null_data)
        assert result == []
