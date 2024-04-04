"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
from . import helper


def test_store_load():
	"""
	Tests the Store_Load API Call
	"""

	helper.provision_store('Store_Load.xml')

	store_load_test_load()
	store_load_test_load_MMAPI194()


def store_load_test_load():
	request = merchantapi.request.StoreLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.StoreLoad)

	assert isinstance(response.get_store(), merchantapi.model.Store)


def store_load_test_load_MMAPI194():
	request = merchantapi.request.StoreLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.StoreLoad)

	assert response.get_store().get_box_packing_id() > 0
	assert response.get_store().get_address_validation_id() > 0