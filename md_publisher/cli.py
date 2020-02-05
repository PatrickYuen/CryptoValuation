import asyncio

import click
import traceback
import yaml

from md_publisher import publishers


async def main(inst_config):
    pub_class_name = inst_config["publisher"]
    pub_class = getattr(publishers, pub_class_name)
    publisher = pub_class(inst_config)
    completed = False

    while not completed:
        try:
            with publisher:
                await publisher.connection
                completed = True
        except Exception as e:
            print("Waiting 10 seconds after:", e)
            traceback.print_tb(e.__traceback__)
            await asyncio.sleep(10)

    print("Finished")


@click.command()
@click.option("--config_path", "-c", help="Full file path of config yaml")
@click.option("--instance", "-i", help="Instance of publisher")
@click.option("--log_path", "-l", default="log", help="Full file path for logging location (TODO)")
def entry_point(config_path, instance, log_path):

    with open(config_path) as fh:
        app_config = yaml.safe_load(fh)
        inst_config = app_config[instance]

    asyncio.run(main(inst_config))


if __name__ == "__main__":
    entry_point()
