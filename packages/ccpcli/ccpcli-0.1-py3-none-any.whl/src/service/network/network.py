###############################################################################
# Copyright (c) 2024-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Mani Keshari <mani@coredge.io>, March 2024                       #
###############################################################################
import os

import click
from src.util.constants import Constants
from src.util.http_helper import delete_assert
from src.util.http_helper import get_assert
from src.util.utils import print_cli, print_info
from src.util.utils import set_context
from src.resource_schemas.network import network_list_response, network_describe_response


@click.group(name=Constants.COMMAND_GROUP_NETWORK)
@click.pass_context
def networks(ctx):
    """This command will do all the operations on networks"""
    pass


@networks.command(name=Constants.COMMAND_GET)
@click.pass_context
@click.option('--output', '-o', help='Supported formats are json,tabular,yaml', required=False)
def get_network(ctx, output):
    """This command will provide the list of Network"""

    # set up the configuration details into ctx object
    set_context(ctx)

    params = {'external': False}
    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}networks'
    res = get_assert(ctx, url=url, params=params)

    if output == Constants.TABULAR_OUTPUT:
        network_list = network_list_response(res)
    else:
        network_list = res
    print_cli(msg=network_list, output_format=output, headers=Constants.TABLE_HEADER_NETWORKS)


@networks.command(name=Constants.COMMAND_DESCRIBE)
@click.pass_context
@click.argument('network')
@click.option('--output', '-o', help='Supported formats are json,tabular,yaml', required=False)
def describe_network(ctx, network, output):
    """This command will describe network"""
    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}networks{os.sep}{network}/'
    res = get_assert(ctx, url=url)

    if output == Constants.TABULAR_OUTPUT:
        network_get = network_describe_response(res)
    else:
        network_get = res
    print_cli(msg=[network_get], output_format=output, headers=Constants.TABLE_HEADER_NETWORK_DESCRIBE)


@networks.command(name=Constants.COMMAND_DELETE)
@click.pass_context
@click.argument('network')
def delete_network(ctx, network):
    """This command will delete instance"""

    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}networks{os.sep}{network}/'

    delete_assert(ctx, url=url, expected_response_code=200)

    print_info(msg="Network deleted successfully")


