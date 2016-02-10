#!/usr/bin/env python
#coding: utf-8
#
# Copyright 2016, Marcos Salomão.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
__author__ = "Marcos Salomão"
__email__ = "salomao.marcos@gmail.com"
__copyright__ = "Copyright 2016, Marcos Salomão"
__license__ = "Apache 2.0"

import logging
import datetime

from app import user
from app.marketplace import models as marketplace

from google.appengine.ext import ndb

#from app.supplier import models
#from app.product import models


class PurchaseModel(ndb.Model):
	"""Entidade representa a compra de um produto pela loja"""

	#Fornecedor	
	supplier = ndb.StringProperty(required=True, indexed=False)
	#ndb.StructuredProperty(SupplierModel, required=True, repeated=False)
	
	#Produto 
	product = ndb.StringProperty(required=True, indexed=False)
	#ndb.StructuredProperty(ProductModel, required=True, repeated=False)

	#Qtidade	
	quantity = ndb.IntegerProperty(required=True, default=1)

	#Data Compra 	
	purchase_date = ndb.DateTimeProperty(required=True, default=datetime.datetime.today())

	#Data Recebimento 	
	received_date = ndb.DateTimeProperty()

	#Valor Unidade 	
	cost = ndb.FloatProperty(required=True)

	#Valor Total	
	total_cost = ndb.FloatProperty()

	#Cambio	USD
	exchange_dollar = ndb.FloatProperty()

	#Valor Unidade USD	
	cost_dollar = ndb.FloatProperty()

	#Valor Total USD	
	total_cost_dollar = ndb.FloatProperty()
		
	#Frete	
	shipping_cost = ndb.FloatProperty()

	#Cód Rastreamento	
	track_code = ndb.StringProperty(indexed=False)

	#Descrição Fatura Cartão 
	invoice = ndb.StringProperty(indexed=False)

	#Data criação
	created_date = ndb.DateTimeProperty(auto_now_add=True)

def list():
	"""Listar compras cadastradas para a loja do usuário.
	"""

	logging.debug("Listando compras cadastradas")

	#Identificando usuário da requisição
	email = user.get_current_user().email()

	logging.debug("Obtendo a entidade da loja para o usuario %s", email)

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get(email)

	#Realizando query, listando as compras
	purchases = PurchaseModel.query(ancestor=marketplaceModel.key).fetch()

	logging.debug("Foram selecionada(s) %d compra(s) para a loja do usuário %s", len(purchases), email)

	#Retornando
	return purchases


def put(purchase):
	"""Inclui ou atualiza uma compra.
	"""

	logging.debug("Persistindo uma compra na loja")

	#Identificando usuário da requisição
	email = user.get_current_user().email()

	logging.debug("Obtendo a entidade da loja para o usuario %s", email)

	#Obtendo marketplace como parent
	marketplaceModel = marketplace.get(email)

	logging.debug("Loja encontrada com sucesso")

	logging.debug("Criando model para a compra ou selecionando o existente para atualizá-lo")

	if purchase.id is not None:
		purchaseModel = ndb.Key('PurchaseModel', purchase.id).get()
	else:
		purchaseModel = PurchaseModel(parent=marketplaceModel.key)

	#Criando model
	purchaseModel.supplier = purchase.supplier
	purchaseModel.product = purchase.product
	purchaseModel.quantity = purchase.quantity
	purchaseModel.purchase_date = purchase.purchase_date
	purchaseModel.received_date = purchase.received_date
	purchaseModel.cost = purchase.cost
	purchaseModel.total_cost = purchase.total_cost
	purchaseModel.exchange_dollar = purchase.exchange_dollar
	purchaseModel.cost_dollar = purchase.cost_dollar
	purchaseModel.total_cost_dollar = purchase.total_cost_dollar
	purchaseModel.shipping_cost = purchase.shipping_cost
	purchaseModel.track_code = purchase.track_code
	purchaseModel.invoice = purchase.invoice

	logging.debug("Persistindo compra...")

	#Persistindo
	purchaseModel.put()

	logging.debug("Persistida compra %d com sucesso na loja ", 
		purchaseModel.key.id(), marketplaceModel.name)

	return purchaseModel