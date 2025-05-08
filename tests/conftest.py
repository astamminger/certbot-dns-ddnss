# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(scope='function')
def ddnssclient():
    from certbot_dns_ddnss.dns_ddnss import _DDNSSClient
    yield _DDNSSClient(api_token=None)


@pytest.fixture(scope='function')
def urlopen_return(monkeypatch):
    from urllib import request

    def mock_urlopen(url, *args, **kwargs):
        return url
    monkeypatch.setattr(request, 'urlopen', mock_urlopen)


@pytest.fixture(scope='function')
def response_with_ok_header(monkeypatch):
    from urllib import request
    # copy 'original' urlopen so that we can use this copy inside the mocked
    # function without running into a max. recursion depth error
    original_urlopen = request.urlopen

    def mock_urlopen(*args, **kwargs):
        # get the original response from urlopen
        response = original_urlopen(*args, **kwargs)
        # set status to '200' and add the expected header that is returned
        # by the API after the TXT record was updated successfully
        response.status = 200
        response.headers.add_header('DDNSS-Message',
                                    'Your hostname has been updated')
        return response
    monkeypatch.setattr(request, 'urlopen', mock_urlopen)
