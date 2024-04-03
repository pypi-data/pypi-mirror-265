import argparse

from exp_heatmap.prepare import prepare
from exp_heatmap.compute import compute
from exp_heatmap.plot import plot


def main():
    parser = argparse.ArgumentParser(
        prog="exp_heatmap",
    )
    subparser = parser.add_subparsers()

    parser.set_defaults(func=lambda _: parser.print_help())

    
    # prepare
    prepare_parser = subparser.add_parser("prepare")
    prepare_parser.add_argument(
        "recode_file", metavar="RECODE_FILE", help="Where is recoded VCF"
    )
    prepare_parser.add_argument(
        "zarr_dir", metavar="ZARR_DIR", help="Where ZARR dir will be saved"
    )
    prepare_parser.set_defaults(
        func=lambda args: prepare(args.recode_file, args.zarr_dir)
    )


    # compute
    compute_parser = subparser.add_parser("compute")
    compute_parser.add_argument(
        "zarr_dir", metavar="ZARR_DIR", help="Where is the ZARR dir located"
    )
    compute_parser.add_argument(
        "panel_file", metavar="PANEL_FILE", help="Where is the panel file located"
    )
    compute_parser.add_argument(
        "output_dir", metavar="OUTPUT_DIR", help="What directory will be the output saved in"
    )
    compute_parser.add_argument(
        "-t", "--test", metavar="TEST", default="xpehh", required=False, help="What test will be computed (default: %(default)s). Possible values are: 'xpehh', 'xpnsl', 'delta_tajima_d', 'hudson_fst'."
    )
    compute_parser.set_defaults(
        func=lambda args: compute(args.zarr_dir, args.panel_file, args.output_dir, args.test)
    )


    # plot
    plot_parser = subparser.add_parser("plot")
    plot_parser.add_argument(
        "input_dir", metavar="INPUT_DIR", help="What files to use as input for drawing of the ExP heatmap, i.e. where is the output dir from previous step ('exp_heatmap compute') located. This contains *.tsv files of pairwise parameters that will serve as input data for plotting."
    )
    plot_parser.add_argument("--begin", type=int, required=True, help="Beginning of displayed area")
    plot_parser.add_argument("--end", type=int, required=True, help="End of displayed area")
    plot_parser.add_argument("--title", default=None, help="Title of the figure")
    plot_parser.add_argument("--output", required=True, default="ExP_heatmap", help="The figure will be saved as OUTPUT + .png")
    plot_parser.set_defaults(
        func=lambda args: plot(
            args.input_dir,
            begin=args.begin,
            end=args.end,
            title=args.title,
            output=args.output,
        )
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
