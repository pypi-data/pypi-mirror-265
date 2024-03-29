import asyncio
import sys
import click
import datetime as dtm
import os
import re
import qupiato.cli.config as c

from qupiato.cli.utils import create_and_upload_to_gcs_bucket, get_token, ws_api_call, get_version, get_agent


@click.group()
def main():
    pass


@main.command()
@click.argument('entryfile')
def deploy(entryfile):
    """Deploy strategy

    ENTRYFILE is the file to deploy
    """
    if not os.path.exists(entryfile):
        click.echo(f"File {entryfile} does not exist")
        return

    # if strategy name is not specified, use the filename without extension
    strategy_name = os.path.splitext(os.path.basename(entryfile))[0]

    # replace all uppercase letters with lowercase
    strategy_name = strategy_name.lower()
    # replace all non-alphabets with hyphens
    strategy_name = re.sub(r'[^a-z0-9]', '-', strategy_name)
    # replace underbars with hyphens
    strategy_name = re.sub(r'_', '-', strategy_name)
    # remove leading and trailing hyphens
    strategy_name = strategy_name.strip('-')

    if not re.match(f'[a-z0-9-]', strategy_name):
        click.echo("Invalid strategy name")
        return

    click.echo(f"Deploying {entryfile} as {strategy_name}")

    asyncio.run(deploy_strategy(entryfile, strategy_name))


async def deploy_strategy(entryfile, strategy_name):
    click.echo(f"Uploading {entryfile} to GCS bucket")
    zipfile = create_and_upload_to_gcs_bucket()

    req = {
        "action": "deploy",
        "strategy_name": strategy_name,
        "token": get_token(),
        "zipfile": zipfile,
        "entryfile": os.path.basename(entryfile),
        "agent": {
            **get_agent()
        }
    }

    async for line in ws_api_call(req):
        if 'text' in line:
            click.echo(line['text'])


@main.command()
def list():
    """ List deployed strategies """

    asyncio.run(list_strategies())


async def list_strategies():
    req = {
        "action": "list",
        "token": get_token(),
    }

    def __calc_column_width(arr, key, title, margin=2):
        max_len = max(len(x[key]) for x in arr)
        max_len = max(max_len, len(title))
        return max_len + margin


    async for r in ws_api_call(req):
        if 'data' not in r:
            continue

        if len(r['data']) == 0:
            click.echo("No strategies deployed")
            return

        data = r['data']

        name_width = __calc_column_width(data, 'name', "DEPLOYMENT ID")
        strategy_width = __calc_column_width(data, 'strategy_name', "STRATEGY NAME")
        status_width = __calc_column_width(data, 'status', "STATUS")

        click.echo(f"{'DEPLOYMENT ID':<{name_width}} {'STRATEGY NAME':<{strategy_width}} {'STATUS':<{status_width}} CREATED AT")

        for e in data:
            created_at = dtm.datetime.fromtimestamp(e['created_at']/1000).strftime('%Y-%m-%d %H:%M:%S')
            click.echo(f"{e['name']:<{name_width}} {e['strategy_name']:<{strategy_width}} {e['status']:<{status_width}} {created_at}")



@main.command()
@click.argument('deployment_id')
def delete(deployment_id):
    """ Delete a deployed strategy """

    asyncio.run(delete_strategy(deployment_id))


async def delete_strategy(deployment_id):
    req = {
        "action": "delete",
        "deployment_id": deployment_id,
        "token": get_token(),
        "agent": {
            **get_agent()
        }
    }

    async for line in ws_api_call(req):
        if 'text' in line:
            click.echo(line['text'])


@main.command()
@click.argument('deployment_id')
@click.option('--follow', '-f', is_flag=True, help="Specify to stream the logs")
@click.option('--lines', '-n', default=None, help="Number of lines to show")
def logs(deployment_id, follow, lines):
    """ Show logs of a deployed strategy """

    asyncio.run(show_logs(deployment_id, follow, lines))


async def show_logs(deployment_id, follow, lines):
    req = {
        "action": "logs",
        "deployment_id": deployment_id,
        "token": get_token(),
        "follow": follow,
    }

    if lines is not None:
        try:
            req['lines'] = int(lines)
        except ValueError:
            click.echo("Invalid value for --lines")
            return

    fetching = True
    while fetching:
        async for line in ws_api_call(req):
            if 'text' in line:
                print(line['text'], end='')

        if req['follow']:
            req['lines'] = 0
            await asyncio.sleep(0.01)
        else:
            fetching = False

@main.command()
def version():
    """ Show version number and quit """
    version = get_version()
    click.echo(f"v{version}")

if __name__ == '__main__':
    main()
