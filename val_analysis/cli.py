import asyncio

import click
import yaml
from contextlib import ExitStack

from val_analysis.publishers import PlotPublisher
from val_analysis.controllers import StrategyController
from val_analysis.reactors import MarketReactor


async def main(app_config):
    # Publisher
    publisher = PlotPublisher(app_config)
    # Controller
    controller = StrategyController(app_config, publisher)
    # Reactor
    reactor = MarketReactor(app_config, controller)

    with ExitStack() as stack:
        stack.enter_context(publisher)
        stack.enter_context(reactor)

        print('Start Service')
        await reactor.connection

    print("Finished")


@click.command()
@click.option("--config_path", "-c", help="Full file path of config yaml")
@click.option("--log_path", "-l", default="log", help="Full file path for logging location (TODO)")
def entry_point(config_path, log_path):

    with open(config_path) as fh:
        app_config = yaml.safe_load(fh)

    asyncio.run(main(app_config))


if __name__ == "__main__":
    entry_point()
