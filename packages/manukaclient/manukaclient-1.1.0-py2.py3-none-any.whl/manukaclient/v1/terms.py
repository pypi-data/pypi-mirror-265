#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from nectarclient_lib import base


class Terms(base.Resource):

    date_fields = ['issued']

    def __repr__(self):
        return "<Terms %s>" % self.id


class TermsManager(base.BasicManager):

    base_url = 'v1/terms'
    resource_class = Terms

    def current(self):
        return self._get('/%s/current/' % self.base_url)
