"""leaf-lesion analysis."""

import os
import logging
import argparse
import errno

from dtoolcore import DataSet

from jicbioimage.core.image import Image
from jicbioimage.core.transform import transformation
from jicbioimage.core.io import AutoName, AutoWrite

__version__ = "0.1.0"

AutoName.prefix_format = "{:03d}_"


def safe_mkdir(directory):
    """Create directories if they do not exist."""
    try:
        os.makedirs(directory)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise


def item_output_path(output_directory, rel_path):
    """Return item output path; and create it if it does not already exist."""
    abs_path = os.path.join(output_directory, rel_path)
    safe_mkdir(abs_path)
    return abs_path


@transformation
def identity(image):
    """Return the image as is."""
    return image


def analyse_file(fpath, output_directory):
    """Analyse a single file."""
    logging.info("Analysing file: {}".format(fpath))

    AutoName.directory = output_directory

    image = Image.from_file(fpath)
    image = identity(image)


def analyse_dataset(dataset_dir, output_dir):
    """Analyse all the files in the dataset."""
    dataset = DataSet.from_path(dataset_dir)
    logging.info("Analysing items in dataset: {}".format(dataset.name))

    for i in dataset.identifiers:
        data_item_abspath = dataset.abspath_from_identifier(i)
        item_info = dataset.item_from_identifier(i)

        specific_output_dir = item_output_path(output_dir, item_info["path"])
        analyse_file(data_item_abspath, specific_output_dir)


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dataset", help="Input dataset")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Write out intermediate images")
    args = parser.parse_args()

    # Create the output directory if it does not exist.
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    AutoName.directory = args.output_dir

    # Only write out intermediate images in debug mode.
    if not args.debug:
        AutoWrite.on = False

    # Setup a logger for the script.
    log_fname = "audit.log"
    log_fpath = os.path.join(args.output_dir, log_fname)
    logging_level = logging.INFO
    if args.debug:
        logging_level = logging.DEBUG
    logging.basicConfig(filename=log_fpath, level=logging_level)

    # Log some basic information about the script that is running.
    logging.info("Script name: {}".format(__file__))
    logging.info("Script version: {}".format(__version__))

    # Run the analysis.
    if os.path.isdir(args.input_dataset):
        analyse_dataset(args.input_dataset, args.output_dir)
    else:
        parser.error("{} not a directory".format(args.input_dataset))

if __name__ == "__main__":
    main()
