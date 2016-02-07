#!/usr/bin/env python
#coding: utf-8
#
# Copyright 2016 Google Inc.
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

"""Python MarketPlace API """

# Importando sys e ajustando o encode para UTF-8, afim de contemplar acentuação
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import endpoints

import app.marketplace.services as marketplace


# Creating api server to bind in app.yaml
APPLICATION = endpoints.api_server([marketplace.MarketplaceService])