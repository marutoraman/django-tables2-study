from django.urls import reverse
from syuppin.views.syuppin import *
import pytest

@pytest.mark.django_db(transaction=True)
def test_fetch_item(self):
    res = self.client.get(reverse("syuppin:list"))
    assert res.status_code == 200