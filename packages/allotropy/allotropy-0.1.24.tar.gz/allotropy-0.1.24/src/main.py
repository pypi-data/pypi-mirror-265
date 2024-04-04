import json

from allotropy.parser_factory import Vendor
from allotropy.to_allotrope import allotrope_from_file

if __name__ == "__main__":
    for output_file in (
        # "appbio_quantstudio_designandanalysis_QS7Pro_Presence_and_Absence_example10.xlsx",
        "example.xlsx",
    ):
        test_filepath = f"../tests/parsers/appbio_quantstudio_designandanalysis/testdata/{output_file}"
        allotrope_dict = allotrope_from_file(
            test_filepath, Vendor.APPBIO_QUANTSTUDIO_DESIGNANDANALYSIS
        )
        print(json.dumps(allotrope_dict, indent=4, ensure_ascii=False))  # noqa: T201
