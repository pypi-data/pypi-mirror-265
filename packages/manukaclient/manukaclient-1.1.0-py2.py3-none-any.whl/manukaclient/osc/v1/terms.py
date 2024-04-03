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

import logging

from nectarclient_lib import exceptions
from osc_lib.command import command
from osc_lib import utils as osc_utils


class ListTerms(command.Lister):
    """List terms."""

    log = logging.getLogger(__name__ + '.ListTerms')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        terms = client.terms.list()
        columns = ['id', 'issued']
        return (
            columns,
            (osc_utils.get_item_properties(q, columns) for q in terms)
        )


class TermsCommand(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(TermsCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help=('ID of terms')
        )
        return parser


class ShowTerms(TermsCommand):
    """Show terms details."""

    log = logging.getLogger(__name__ + '.ShowTerm')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            term = client.terms.get(parsed_args.id)
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(term.to_dict())


class CurrentTerms(command.ShowOne):
    """Show current terms details."""

    log = logging.getLogger(__name__ + '.ShowTerm')

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.account
        try:
            term = client.terms.current()
        except exceptions.NotFound as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(term.to_dict())
