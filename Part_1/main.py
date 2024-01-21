import argparse
import logging
from pathlib import Path
from shutil import copyfile
import concurrent.futures


parser = argparse.ArgumentParser(
    prog="Assistant-sorter",
    description="Application helps to sort the files in the directory",
)

parser.add_argument("-s", "--source", required=True)
parser.add_argument("-d", "--destination", default="Destination")

args = vars(parser.parse_args())

source = args.get("source")
destination = args.get("destination")

directories = []


def scans_directories(path: Path):
    for obj in path.iterdir():
        if obj.is_dir():
            directories.append(obj)
            scans_directories(obj)


def sorts_files(path: Path):
    logging.debug(f'Started sorting the directory: "{path}".')
    for obj in path.iterdir():
        if obj.is_file():
            try:
                if obj.suffix:
                    new_path = destination_directory / obj.suffix
                    new_path.mkdir(exist_ok=True, parents=True)
                    copyfile(obj, new_path / obj.name)
                else:
                    other_path = destination_directory / "OTHERS"
                    other_path.mkdir(exist_ok=True)
                    copyfile(obj, other_path / obj.name)
            except OSError as e:
                logging.error(e)
    logging.debug(f'Finished sorting the directory: "{path}".')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    base_directory = Path(source)
    destination_directory = Path(destination)

    directories.append(base_directory)
    scans_directories(base_directory)

    print(f"Directories: {directories}")

    with concurrent.futures.ThreadPoolExecutor(
        thread_name_prefix="Thread", max_workers=4
    ) as executor:
        results = list(
            executor.map(sorts_files, [directory for directory in directories])
        )

    logging.debug(
        f'{["Files in directory: " + str(directory) + " have been sorted." for directory in directories]}'
    )

    print(
        f'All files in directory "{base_directory}" have been sorted successfully and copied to directory: '
        f'"{destination_directory}".\n"{base_directory}" directory can be removed.'
    )
