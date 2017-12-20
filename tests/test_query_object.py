import pytest
from ah_dns_helper import QueryObject

def test_no_query_string():
    with pytest.raises(TypeError):
        qo = QueryObject()

def test_domain():
    qo = QueryObject('google.com')

    assert 'That is actually a domain' in str(qo)

def test_url():
    qo = QueryObject('https://google.com')

    assert 'That actually looks like a url' in str(qo)

