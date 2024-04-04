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


def test_productvariantpricing_update():
	"""
	Tests the ProductVariantPricing_Update API Call
	"""

	helper.provision_store('ProductVariantPricing_Update.xml')

	productvariantpricing_update_test_update()


def productvariantpricing_update_test_update():
	product = helper.get_product('ProductVariantPricing_Update')

	assert product is not None

	variants = helper.get_product_variants('ProductVariantPricing_Update')

	assert len(variants) == 1

	request = merchantapi.request.ProductVariantPricingUpdate(helper.init_client(), product)

	request.set_variant_id(variants[0].get_variant_id())
	request.set_method(merchantapi.request.ProductVariantPricingUpdate.VARIANT_PRICING_METHOD_SUM)
	request.set_price(2.22)
	request.set_cost(1.11)
	request.set_weight(3.33)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantPricingUpdate)

	check = helper.get_variant_pricing(product.get_id(), variants[0].get_variant_id())

	assert check is not None

	assert check['price'] == 2.22
	assert check['cost'] == 1.11
	assert check['weight'] == 3.33
	assert check['method'] == 2
