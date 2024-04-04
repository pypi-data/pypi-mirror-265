import json
import sys

sys.path += ["/Users/alejo/allotropy", "/Users/alejo/allotropy/src"]

from allotropy.parser_factory import Vendor  # noqa: E402
from tests.parsers.test_utils import from_file  # noqa: E402

file_name = "appbio_quantstudio_designandanalysis_QS1_Standard_Curve_example01.xlsx"


test_filepath = (
    f"../tests/parsers/appbio_quantstudio_designandanalysis/testdata/{file_name}"
)
allotrope_dict = from_file(test_filepath, Vendor.APPBIO_QUANTSTUDIO_DESIGNANDANALYSIS)

print(json.dumps(allotrope_dict, indent=4, ensure_ascii=False))  # noqa: T201
