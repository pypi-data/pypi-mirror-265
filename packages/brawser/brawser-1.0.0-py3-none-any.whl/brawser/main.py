import click

from brawser.open_console import open_console

@click.command(help="The simplest browser opener with AWS management console from the command line interface.")
@click.version_option()
@click.option("-h", "--hours", required=False, default=3,
              help="Set session hours. The default is 3 hours")
@click.option("-p", "--print-url", required=False, is_flag=True,
              help="Print the federated URL (optional)")
@click.option("-c", "--copy-clipboard", required=False, is_flag=True,
              help="Copy the federated URL when you use MacOS only (optional)")
def cmd(hours, print_url, copy_clipboard):
    open_console(hours, print_url, copy_clipboard)

def main():
    cmd()

if __name__ == '__main__':
    main()
