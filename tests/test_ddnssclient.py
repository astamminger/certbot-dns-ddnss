"""
Test Suite for _DDNSSClient Tests
"""


import pytest


def test_get_ddnss_api_base_url(ddnssclient):
    """Test for correct API base domain"""
    expected_api_base_url = "https://www.ddnss.de/upd.php"
    returned_api_base_url = ddnssclient.get_ddnss_api_base_url()
    assert returned_api_base_url == expected_api_base_url

def test_get_api_request_add_params(ddnssclient):
    """Test returned parameter set for add TXT requests"""
    api_token = "a1b2c3d4"
    domain = "example.com"
    txt_record = "dns_txt_record"
    params = ddnssclient.get_api_request_add_params(api_token, domain,
                                                    txt_record)
    # check that dict is returned
    assert isinstance(params, dict)
    # pop all expected keys from the dictionary
    returned_api_token = params.pop("key")
    assert returned_api_token == api_token
    returned_domain = params.pop("host")
    assert returned_domain == domain
    returned_api_type = params.pop("txtm")
    assert returned_api_type == 1
    returned_txt_record = params.pop("txt")
    assert returned_txt_record == txt_record
    # finally check that dict is empty
    assert len(params) == 0

def test_get_api_request_del_params(ddnssclient):
    """Test returned parameter set for add TXT requests"""
    api_token = "a1b2c3d4"
    domain = "example.com"
    params = ddnssclient.get_api_request_del_params(api_token, domain)
    # check that dict is returned
    assert isinstance(params, dict)
    # pop all expected keys from the dictionary
    returned_api_token = params.pop("key")
    assert returned_api_token == api_token
    returned_domain = params.pop("host")
    assert returned_domain == domain
    returned_api_type = params.pop("txtm")
    assert returned_api_type == 2
    # finally check that dict is empty
    assert len(params) == 0

def test_get_api_request_for_params_add(ddnssclient):
    """Test the generated API url for adding TXT records"""
    base_url = "https://www.ddnss.de/upd.php"
    api_token = "a1b2c3d4"
    domain = "example.com"
    txt_record = "dns_txt_record"
    expected_api_url = (f"{base_url}?key={api_token}&host={domain}&txtm=1&"
                        f"txt={txt_record}")
    add_params = ddnssclient.get_api_request_add_params(api_token, domain,
                                                        txt_record)
    generated_api_url = ddnssclient.get_api_request_for_params(add_params)
    assert generated_api_url == expected_api_url

def test_get_api_request_for_params_del(ddnssclient):
    """Test the generated API url for deleting TXT records"""
    base_url = "https://www.ddnss.de/upd.php"
    api_token = "a1b2c3d4"
    domain = "example.com"
    expected_api_url = f"{base_url}?key={api_token}&host={domain}&txtm=2"
    del_params = ddnssclient.get_api_request_del_params(api_token, domain)
    generated_api_url = ddnssclient.get_api_request_for_params(del_params)
    assert generated_api_url == expected_api_url
