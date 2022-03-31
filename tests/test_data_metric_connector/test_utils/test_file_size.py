from data_metric_connector.utils.file_size import convert_size


def test_convert_size():
    assert convert_size(1024) == "1.0 KB"


def test_convert_size_zero():
    assert convert_size(0) == "0B"
