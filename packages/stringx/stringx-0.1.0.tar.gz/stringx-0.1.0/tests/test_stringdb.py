import pytest
import httpx

import stringdb


# @pytest.mark.parametrize(
#     "identifiers,string_id",
#     [
#         ("edin", "7227.FBpp0074940"),
#     ],
# )
def test_map_identifiers(httpx_mock):
    httpx_mock.add_response(
        # url=httpx.URL(
        #     "api/json/get_string_ids", params={"identifiers": "edin", "species": "7227"}
        # ),
        # method="POST",
        json={"queryItem": "edin", "stringId": "7227.FBpp0074940"},
    )

    identifiers = stringdb.map_identifiers(["edin"], 7227)

    assert identifiers

    print(identifiers)

    assert 0
    # for result in results:
    #     assert result["queryItem"] == query
    #     assert result["stringId"] == string_id


@pytest.mark.xfail
def test_map_multiple():
    assert 0
