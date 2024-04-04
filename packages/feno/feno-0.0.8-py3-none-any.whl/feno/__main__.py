import argparse
import sys
import os

from .actions import Actions
from .__init__ import __version__
from .log import Log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('targets', metavar='T', type=str, nargs='*', help='Readmes or folders')
    parser.add_argument("--check", "-c", action="store_true", help="Check if the file needs to be rebuilt")
    parser.add_argument("--preamble", "-p", action="store_true", help="disable qxcode preamble")
    parser.add_argument("--version", action="store_true", help="Prints the version")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose mode")
    parser.add_argument("--keep", "-k", action="store_true", help="Keep the cache files")
    parser.add_argument("--remote", "-r", type=str, help="remote config file")
    
    args = parser.parse_args()
    Log.set_verbose(args.verbose)
    
    if args.version:
        print(__version__)
        sys.exit(0)

    if len(args.targets) == 0:
        print("fail: No targets specified")
        exit(1)

    for target in args.targets:
        hook = os.path.basename(os.path.abspath(target))

        actions = Actions(target, args.remote)
        Log.resume(hook, end=": [ ")
        Log.verbose(hook, end=": ")

        if not actions.validate():
            continue

        actions.load_title()
        actions.create_cache()
        actions.update_markdown()

        if not args.check or actions.need_rebuild():
            actions.recreate_cache() # erase .cache
            actions.remote_md(args.preamble)
            actions.html()
            actions.build_cases()
            actions.copy_drafts()
            actions.run_local_sh()
            actions.init_vpl()
            actions.create_mapi()
            actions.clean(args.keep)

        Log.resume("]")


if __name__ == "__main__":
    main()
