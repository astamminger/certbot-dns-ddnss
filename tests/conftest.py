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
