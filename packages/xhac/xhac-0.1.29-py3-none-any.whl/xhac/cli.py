from rich.console import Console
from rich.table import Table
from rich import box
from typing import Union, Any
import click
import json
from .client import HomeClient, HACException
from .scanner import Scanner

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def get_version():
    from pkg_resources import get_distribution
    return get_distribution("xhac").version


def print_version(
    context: click.Context, param: Union[click.Option, click.Parameter], value: bool
) -> Any:
    """Print the version of mbed-tools."""
    if not value or context.resilient_parsing:
        return
    click.echo(get_version())
    context.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Display versions.",
)
def cli() -> None:
    """The MXCHIP Home Access Client Tool."""
    pass


@click.command()
def scan() -> None:
    """Scan for MXCHIP Home Access Server on local network.

    Example:

        $ xhac scan
    """
    scanner = Scanner()
    click.echo("Scanning for servers ...")
    scanner.scan()

    if len(scanner.servers) == 0:
        click.echo("No server found")
        return

    table = Table(title="Servers", box=box.ROUNDED)
    table.add_column("Name")
    table.add_column("Model")
    table.add_column("MAC")
    table.add_column("IP")
    for index, server in enumerate(scanner.servers):
        table.add_row(
            server.name, server.model, server.mac, f"{server.ip}"
        )
    console = Console()
    console.print(table)


@click.command()
@click.argument("ip", type=click.STRING)
@click.argument("password", type=click.STRING, default="haspwd")
@click.option("-s", "--save", type=click.STRING)
def info(ip: str, password: str, save: str) -> None:
    """Connect to HAS and Get Home model.

    Arguments:

        IP: IPv4 address. eg, 192.168.31.66

        PASSWORD: Password of the server, default is "haspwd".

        -s/--save: save the home model to a file in JSON format.

    Example:

        $ xhac info 192.168.31.66
    """

    click.echo(f"Connecting to {ip} ...")
    client = HomeClient(ip, 53248, "hasusr", password)

    try:
        client.connect()
    except HACException:
        click.echo("Failed to connect")
        return

    if save:
        with open(save, "w") as f:
            f.write(json.dumps(client._home_db, indent=2, ensure_ascii=False))
        return

    console = Console()

    table = Table(title="Entities", box=box.ROUNDED)
    table.add_column("Name")
    table.add_column("Room")
    table.add_column("MAC")
    for entity in client.entities:
        table.add_row(f"{entity.name}-{entity.sid}", entity.zone, entity.mac)
    console.print(table)

    table = Table(title="Scenes", box=box.ROUNDED)
    table.add_column("Name")
    for scene in client.scenes:
        table.add_row(scene.name)
    console.print(table)


@click.command()
@click.argument("ip", type=click.STRING)
@click.argument("password", type=click.STRING)
@click.argument("did", type=click.INT)
@click.argument("sid", type=click.INT)
@click.argument("typ", type=click.INT)
@click.argument("value", type=click.STRING)
def attr(ip: str, password: str, did: int, sid: int, typ: int, value: str) -> None:
    """Connect to HAS and set attribute

    Arguments:

        IP: IPv4 address. eg, 192.168.31.66

        PASSWORD: Password of the server, default is "haspwd".

        DID: Device ID.

        SID: Service ID.

        typ: Type of the attribute.

        VALUE: Value of the attribute.

    Example:

        $ xhac attr 192.168.31.66 haspwd 66 0 256 1
    """

    click.echo(f"Connecting to {ip} ...")
    client = HomeClient(ip, 53248, "hasusr", password)

    try:
        client.connect()
    except HACException:
        click.echo("Failed to connect")
        return

    click.echo("Setting attribute ...")
    status, _ = client._put(
        "/attributes",
        '{"attributes": [{"did": %d, "sid": %d, "type": %d, "value": %s}]}'
        % (did, sid, typ, value),
    )

    if status == 204:
        click.echo("Successed")
    else:
        click.echo("Failed")


@click.command()
@click.argument("ip", type=click.STRING)
@click.argument("password", type=click.STRING)
@click.argument("sid", type=click.INT)
def scene(ip: str, password: str, sid: int) -> None:
    """Connect to HAS and set scene

    Arguments:

        IP: IPv4 address. eg, 192.168.31.66

        PASSWORD: Password of the server, default is "haspwd".

        SID: Scene ID.

    Example:

        $ xhac scene 192.168.31.66 haspwd 6
    """

    click.echo(f"Connecting to {ip} ...")
    client = HomeClient(ip, 53248, "hasusr", password)

    try:
        client.connect()
    except HACException:
        click.echo("Failed to connect")
        return

    click.echo("Setting scene ...")
    status, _ = client.set_scene(sid)

    if status == 204:
        click.echo("Successed")
    else:
        click.echo("Failed")

def main():
    cli.add_command(scan, "scan")
    cli.add_command(info, "info")
    cli.add_command(attr, "attr")
    cli.add_command(scene, "scene")
    cli()


if __name__ == "__main__":
    main()
