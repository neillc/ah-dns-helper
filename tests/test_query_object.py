import pytest
from ah_dns_helper import QueryObject

def test_no_query_string():
    with pytest.raises(TypeError):
        qo = QueryObject()

def test_domain():
    qo = QueryObject('google.com')

    assert 'That is actually a domain' in str(qo)
