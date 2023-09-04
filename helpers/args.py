import argparse


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(description="----")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo",
        help="Model name to load from the provider.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature parameter for provided model.",
    )
    parser.add_argument(
        "--output_file_name",
        default=None,
        help="Filename to override the default output file name with.",
    )
    parser.add_argument(
        "--input_file_name",
        default=None,
        help="Filename to override the default input file name with.",
    )
    parser.add_argument(
        "--n_samples",
        type=int,
        default=1,
        help="How many prompt data samples to generate for 1 function description.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        help="Choose generation mode from 'snippet', 'description', or 'sample'.",
    )
    return parser.parse_args()
