#!/usr/bin/env python3

from __future__ import annotations
import argparse

from finaletools.frag.frag_length import (
    _cli_frag_length, frag_length_bins, frag_length_intervals
)
from finaletools.utils.filter_bam import filter_bam
from finaletools.frag.coverage import coverage
from finaletools.frag.multi_wps import multi_wps
from finaletools.frag.delfi import delfi
from finaletools.frag.adjust_wps import adjust_wps
from finaletools.frag.agg_wps import agg_wps
from finaletools.frag.delfi_gc_correct import cli_delfi_gc_correct
from finaletools.frag.end_motifs import end_motifs, _cli_mds
from finaletools.frag.cleavage_profile import _cli_cleavage_profile
from finaletools.genome.gaps import _cli_gap_bed

# TODO: implement subcommands read from stdin
# TODO: implement pipelining

def main_cli_parser():
    parser = argparse.ArgumentParser(
        description='Calculates fragmentation features given a CRAM/BAM/SAM '
        'file',
        epilog='')
    subparsers = parser.add_subparsers(title='subcommands',
                                       dest='subcommand')

    # Common arguments

    # Subcommand 1: frag-coverage
    parser_command1 = subparsers.add_parser(
        'coverage',
        description=(
        'Calculates fragmentation coverage over intervals in a BED file given '
        'a BAM/SAM file'
        )
    )
    # TODO: accept tabix

    parser_command1.add_argument(
        'input_file',
        help='BAM or SAM file containing fragment data'
    )
    parser_command1.add_argument(
        'interval_file',
        help='BED file containing intervals over which coverage is calculated'
    )
    parser_command1.add_argument(
        '-o',
        '--output_file',
        default='-',
        help='BED file where coverage is printed'
    )
    parser_command1.add_argument(
        '-s',
        '--scale-factor',
        default=1e6,
        type=float,
        help='Amount coverage will be multiplied by'
    )
    parser_command1.add_argument(
        '-q',
        '--quality_threshold',
        default=30,
        type=int
    )
    parser_command1.add_argument(
        '-w',
        '--workers',
        default=1,
        type=int,
        help='Number of worker processes to use. Default is 1.'
    )
    parser_command1.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=0
    )
    parser_command1.set_defaults(func=coverage)

    # Subcommand 2: frag-length
    parser_command2 = subparsers.add_parser(
        'frag-length', prog='finaletools-frag-length',
        description='Calculates fragment lengths given a CRAM/BAM/SAM file',
        )
    parser_command2.add_argument(
        'input_file',
        type=str,
        help='bam or frag.gz file containing fragment data.',
    )
    parser_command2.add_argument(
        '-c',
        '--contig',
        type=str,
        help='contig or chromosome to select fragments from. Required if '
        'using --start or --stop.',
    )
    parser_command2.add_argument(
        '-S',
        '--start',
        type=int,
        help='0-based left-most coordinate of interval to select fragments'
        'from. Must also use --contig.',
    )
    parser_command2.add_argument(
        '-E',
        '--stop',
        help='1-based right-most coordinate of interval to select fragments'
        'from. Must also use --contig.',
        type=int,
    )
    parser_command2.add_argument(
        '-p',
        '--intersect_policy',
        default='midpoint',
        type=str,
        help='Specifies what policy is used to include fragments in the given '
        'interval. Default is "midpoint". Policies include:\n'
        '- midpoint: the average of end coordinates of a fragment lies'
        'in the interval.\n'
        '- any: any part of the fragment is in the interval.',
    )
    parser_command2.add_argument(
        '-o',
        '--output_file',
        default='-',
        type=str,
        help='File to write results to. "-" may be used to write to stdout. '
        'Default is "-".',
    )
    parser_command2.add_argument(
        '-q',
        '--quality_threshold',
        default=30,
        type=int,
        help="Minimum MAPQ. Default is 30."
    )
    parser_command2.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Verbose logging.'
    )
    parser_command2.set_defaults(func=_cli_frag_length)

    # Subcommand 3: frag_length_bins()
    parser_command3 = subparsers.add_parser(
        'frag-length-bins', prog='finaletools-frag-length-bins',
        description='computes frag lengths of fragments and either prints'
        'bins and counts to tsv or prints a histogram'
        )
    parser_command3.add_argument(
        'input_file',
        help='BAM or SAM file containing fragment data'
    )
    parser_command3.add_argument(
        '-c',
        '--contig',
        type=str,
        help='contig or chromosome to select fragments from. Required if '
        'using --start or --stop.',
    )
    parser_command3.add_argument(
        '-S',
        '--start',
        type=int,
        help='0-based left-most coordinate of interval to select fragments'
        'from. Must also use --contig.',
    )
    parser_command3.add_argument(
        '-p',
        '--intersect_policy',
        default='midpoint',
        type=str,
        help='Specifies what policy is used to include fragments in the given '
        'interval. Default is "midpoint". Policies include:\n'
        '- midpoint: the average of end coordinates of a fragment lies'
        'in the interval.\n'
        '- any: any part of the fragment is in the interval.',
    )
    parser_command3.add_argument(
        '-E',
        '--stop',
        help='1-based right-most coordinate of interval to select fragments'
        'from. Must also use --contig.',
        type=int,
    )
    parser_command3.add_argument(
        '--bin-size',
        type=int,
        help='Used to specify a custom bin size instead of automatically'
        ' calculating one.')
    parser_command3.add_argument(
        '-o',
        '--output_file',
        default='-',
        type=str,
        help='File to write results to. "-" may be used to write to stdout. '
        'Default is "-".',
    )
    parser_command3.add_argument(
        '--contig-by-contig',
        action='store_true',
        help='Placeholder, not implemented.'
    )
    parser_command3.add_argument(
        '--histogram',
        action='store_true',
        help='Draws a histogram in the terminal.'
    )
    parser_command3.add_argument(
        '-q',
        '--quality_threshold',
        default=30,
        type=int,
        help="Minimum MAPQ. Default is 30."
    )
    parser_command3.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Verbose logging.'
    )
    parser_command3.set_defaults(func=frag_length_bins)

    # Subcommand 3_1: frag_length_intervals
    parser_command3_1 = subparsers.add_parser(
        'frag-length-intervals',
        description='Calculates frag lengths statistics for intervals'
    )
    parser_command3_1.add_argument(
        'input_file',
        help='BAM or SAM file containing PE WGS of cfDNA'
    )
    parser_command3_1.add_argument(
        'interval_file',
        help='BED file containing intervals over which to produce statistics'
    )
    parser_command3_1.add_argument(
        '-p',
        '--intersect_policy',
        default='midpoint',
        type=str,
        help='Specifies what policy is used to include fragments in the given '
        'interval. Default is "midpoint". Policies include:\n'
        '- midpoint: the average of end coordinates of a fragment lies'
        'in the interval.\n'
        '- any: any part of the fragment is in the interval.',
    )
    parser_command3_1.add_argument(
        '-o',
        '--output-file',
        default='-',
        help='File to print results to. if "-", will print to stdout. Default'
        'is "-".'
    )
    parser_command3_1.add_argument(
        '-q',
        '--quality-threshold',
        default=30,
        type=int,
        help='minimum MAPQ to filter for'
    )
    parser_command3_1.add_argument(
        '-w',
        '--workers',
        default=1,
        type=int,
        help='Number of subprocesses to use'
    )
    parser_command3_1.add_argument(
        '-v',
        '--verbose',
        default=0,
        action='count',
        help='Determines how much is written to stderr'
    )
    parser_command3_1.set_defaults(func=frag_length_intervals)

    # Subcommand 4: wps (on interval bed file)
    parser_command4 = subparsers.add_parser(
        'wps',
        prog='finaletools-wps',
        description='Calculates Windowed Protection Score over a region '
        'around sites specified in a BED file from alignments in a '
        'CRAM/BAM/SAM file'
    )
    parser_command4.add_argument(
        'input_file',
        help='bam or sam file containing paired-end reads of cfDNA WGS'
    )
    parser_command4.add_argument(
        'site_bed',
        help='bed file containing sites over which to calculate wps'
    )
    parser_command4.add_argument(
        '-o',
        '--output_file',
        default='-',
        help='BigWig file to write results to. Default is stdout'
    )
    parser_command4.add_argument(
        '-i',
        '--interval_size',
        default=5000,
        type=int
    )
    parser_command4.add_argument(
        '-W',
        '--window_size',
        default=120,
        type=int
    )
    parser_command4.add_argument(
        '-lo',
        '--fraction_low',
        default=120,
        type=int
    )
    parser_command4.add_argument(
        '-hi',
        '--fraction_high',
        default=180,
        type=int
    )
    parser_command4.add_argument(
        '-q',
        '--quality_threshold',
        default=30,
        type=int
    )
    parser_command4.add_argument(
        '-w',
        '--workers',
        default=1,
        type=int
    )
    parser_command4.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0)
    parser_command4.set_defaults(func=multi_wps)

    # Subcommand 5: delfi
    parser_command5 = subparsers.add_parser(
        'delfi',
        prog='finaletools-delfi',
        description='Calculates DELFI score over genome'
        )
    parser_command5.add_argument('input_file')
    parser_command5.add_argument('autosomes')
    parser_command5.add_argument('reference_file')
    parser_command5.add_argument('bins_file')
    parser_command5.add_argument('-b', '--blacklist_file')
    parser_command5.add_argument('-g', '--gap_file')
    parser_command5.add_argument('-o', '--output_file')
    parser_command5.add_argument('-W', '--window_size', default=100000, type=int)
    parser_command5.add_argument('-gc', '--gc_correct', action='store_true')
    parser_command5.add_argument('-m', '--merge_bins', action='store_true')
    parser_command5.add_argument('-q', '--quality_threshold', default=30, type=int)
    parser_command5.add_argument('-w', '--workers', default=1, type=int)
    parser_command5.add_argument('-v', '--verbose', action='count', default=0)
    parser_command5.set_defaults(func=delfi)

    # Subcommand 6: filter_bam
    parser_command6 = subparsers.add_parser(
        'filter-bam',
        prog='finaletools-filter-bam',
        description='Filters a BAM file so that all reads are in mapped pairs'
        ', exceed a certain MAPQ, are not flagged for quality, are read1, are'
        ' not secondary or supplementary alignments, and are on the same '
        'reference sequence as the mate.'
    )
    parser_command6.add_argument(
        'input_file',
        help='BAM file with PE WGS'
    )
    parser_command6.add_argument(
        '-r',
        '--region-file',
        default=None,
        help='BED file containing regions to read fragments from. Default is'
        ' None.'
    )
    parser_command6.add_argument(
        '-o',
        '--output-file',
        default='-',
        help='Path to write filtered BAM. Defualt is "-". If set to "-",'
        ' the BAM file will be written to stdout.'
    )
    parser_command6.add_argument(
        '-q',
        '--quality_threshold',
        type=int,
        default=30,
        help='Minimum mapping quality to filter for. Defualt is 30.'
    )
    parser_command6.add_argument(
        '-hi',
        '--fraction-high',
        type=int,
        default=None,
        help='Maximum fragment size. Default is None'
    )
    parser_command6.add_argument(
        '-lo',
        '--fraction-low',
        type=int,
        default=None,
        help='Minimum fragment size. Default is None'
    )
    parser_command6.add_argument(
        '-w',
        '--workers',
        type=int,
        default=1,
        help='Number of worker processes to spawn.'
    )
    parser_command6.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Specify verbosity. Number of printed statements is proportional '
        'to number of vs.'
    )
    parser_command6.set_defaults(func=filter_bam)

    # Subcommand 7: adjust WPS
    parser_command7 = subparsers.add_parser(
        'adjust-wps',
        prog='finaletools-adjust-wps',
        description='Reads WPS data from a WIG file and applies a median filter'
        ' and a Savitsky-Golay filter (Savitsky and Golay, 1964).'
    )
    parser_command7.add_argument(
        'input_file',
        help='BigWig file with WPS data.'
    )
    parser_command7.add_argument(
        'interval_file',
        help='BED file containing intervals over which wps was calculated'
    )
    parser_command7.add_argument(
        'genome_file',
        help='GENOME file containing chromosome/contig names and lengths. '
        'Needed to write head for BigWig.'
    )
    parser_command7.add_argument(
        '-o',
        '--output-file',
        default='-',
        help='WIG file to print filtered WPS data. If "-", will write to '
        'stdout. Default is "-".'
    )
    parser_command7.add_argument(
        '-m',
        '--median-window-size',
        default=1000,
        type=int,
        help='Size of window for median filter. Default is 1000.'
    )
    parser_command7.add_argument(
        '-s',
        '--savgol-window-size',
        default=21,
        type=int,
        help='Size of window for Savitsky-Golay filter. Default is 21.'
    )
    parser_command7.add_argument(
        '-p',
        '--savgol-poly-deg',
        default=2,
        type=int,
        help='Degree polynomial for Savitsky-Golay filter. Default is 2.'
    )
    parser_command7.add_argument(
        '-w',
        '--workers',
        default=1,
        type=int,
        help='Number of subprocesses to use. Default is 1.'
    )
    parser_command7.add_argument(
        '--mean',
        action='store_true',
    )
    parser_command7.add_argument(
        '--subtract-edges',
        action='store_true',
    )
    parser_command7.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Specify verbosity. Number of printed statements is proportional to number of vs.'
    )
    parser_command7.set_defaults(func=adjust_wps)

    # Subcommand 8: aggregate WPS
    parser_command8 = subparsers.add_parser(
        'agg-wps',
        prog='finaletools-agg-wps',
        description='Reads WPS data from a WIG file and aggregates over'
        ' intervals in a BED file.'
    )
    parser_command8.add_argument(
        'input_file',
        help='BigWig file with WPS data.'
    )
    parser_command8.add_argument(
        'interval_file',
        help='BED file containing intervals over which wps was calculated'
    )
    parser_command8.add_argument(
        '-o',
        '--output-file',
        default='-',
        help='WIG file to print filtered WPS data. If "-", will write to '
        'stdout. Default is "-".'
    )
    parser_command8.add_argument(
        '-m',
        '--median-window-size',
        default=1000,
        type=int,
        help='Size of window for median filter. Default is 1000.'
    )
    parser_command8.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Specify verbosity. Number of printed statements is proportional to number of vs.'
    )
    parser_command8.set_defaults(func=agg_wps)

    # Subcommand 9: delfi gc correct
    parser_command9 = subparsers.add_parser(
        'delfi-gc-correct',
        prog='finaletools-delfi-gc-correct',
        description='Performs gc-correction on raw delfi data.'
    )
    parser_command9.add_argument(
        'input_file',
        help='BED3+3 file containing raw data'
    )
    parser_command9.add_argument(
        '-o',
        '--output-file',
        default='-',
        help='BED3+3 to print GC-corrected DELFI fractions. If "-", will write'
        ' to stdout. Default is "-".'
    )
    parser_command9.add_argument(
        '--header-lines',
        default=1,
        type=int,
        help='Number of header lines in BED. Default is 1.'
    )
    parser_command9.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Specify verbosity. Number of printed statements is proportional '
        'to number of vs.'
    )
    parser_command9.set_defaults(func=cli_delfi_gc_correct)

    # Subcommand 10: end motifs
    parser_command10 = subparsers.add_parser(
        'end-motifs',
        prog='finaletools-end-motifs',
        description="Measures frequency of k-mer 5' end motifs and tabulates"
        " data into a tab-delimited file."
    )
    parser_command10.add_argument(
        'input_file',
        help='SAM, BAM, or tabix-indexed file with fragment data.'
    )
    parser_command10.add_argument(
        'refseq_file',
        help='2bit file containing reference sequence that fragments were'
        ' aligned to.'
    )
    parser_command10.add_argument(
        '-k',
        default=4,
        type=int,
        help='Length of k-mer. Default is 4.'
    )
    parser_command10.add_argument(
        '-o',
        '--output-file',
        default='-',
        help='TSV to print k-mer frequencies. If "-", will write'
        ' to stdout. Default is "-".'
    )
    parser_command10.add_argument(
        '-q',
        '--quality-threshold',
        default=20,
        type=int,
        help='Minimum MAPQ of reads. Default is 20.'
    )
    parser_command10.add_argument(
        '-w',
        '--workers',
        default=1,
        type=int,
        help='Number of subprocesses to use. Default is 1.'
    )
    parser_command10.add_argument(
        '-v',
        '--verbose',
        default=0,
        action='count',
        help='Specify verbosity. Number of printed statements is proportional '
        'to number of vs.'
    )
    parser_command10.set_defaults(func=end_motifs)

    # Subcommand 11: MDS
    parser_command11 = subparsers.add_parser(
        'mds',
        prog='finaletools-mds',
        description='Reads k-mer frequencies from a file and calculates a '
        'motif diversity score (MDS) using normalized Shannon entropy as '
        'described by Jiang et al (2020). This function is generalized for '
        'any k-mer instead of just 4-mers.'
    )
    parser_command11.add_argument(
        'file_path',
        nargs='?',
        default='-',
        help='Tab-delimited or similar file containing one column for all '
        'k-mers a one column for frequency. Reads from stdin by default.'
    )
    parser_command11.add_argument(
        '-s',
        '--sep',
        default='\t',
        help='Separator used in tabular file. Default is tab.'
    )
    parser_command11.add_argument(
        '--header',
        default=0,
        type=int,
        help='Number of header rows to ignore. Default is 0'
    )
    parser_command11.set_defaults(func=_cli_mds)

    
    # Subcommand 12: gap bed
    parser_command12 = subparsers.add_parser(
        'gap-bed',
        prog='finaletools-gap-bed',
        description='Creates a BED4 file containing centromeres, '
        'telomeres, and short-arm intervals, similar to the gaps '
        'annotation track for hg19 found on the UCSC Genome Browser '
        '(Kent et al 2002). Currently only supports hg19, b37, '
        'human_g1k_v37, hg38, and GRCh38',
        epilog='Gap is used liberally in this command, and in the case '
        'hg38/GRCh38, may refer to regions where there no longer are '
        'gaps in the reference sequence.'
    )
    parser_command12.add_argument(
        'reference_genome',
        choices=['hg19', 'b37','human_g1k_v37', 'hg38', 'GRCh38'],
        help='Reference genome to provide gaps for.'
    )
    parser_command12.add_argument(
        'output_file',
        help='Path to write bed file to. If "-" used, writes to stdout.'
    )
    parser_command12.set_defaults(func=_cli_gap_bed)

    # Subcommand 13: cleavage profile
    parser_command13 = subparsers.add_parser(
        'cleavage-profile',
        prog='finaletools-cleavage-profile',
        description='wip'
    )
    parser_command13.add_argument(
        'input_file',
        help='BAM, CRAM, or frag.gz containing fragment coordinates.'
    )
    parser_command13.add_argument(
        'interval_file',
        help='BED file containing intervals to calculate cleavage profile '
        'over.'
    )
    parser_command13.add_argument(
        '-o',
        '--output_file',
        default='-',
        help='Path to write output file to. If "-" used, writes bed.gz to '
        'stdout. Writes in BigWig format if ".bw" or ".bigwig" used, and '
        'writes in gzip compressed bed file if ".bed.gz" or ".bedGraph.gz" '
        'suffixes used. Default is "-".',
    )
    parser_command13.add_argument(
        '-lo',
        '--fraction_low',
        default=120,
        type=int
    )
    parser_command13.add_argument(
        '-hi',
        '--fraction_high',
        default=180,
        type=int
    )
    parser_command13.add_argument(
        '-q',
        '--quality-threshold',
        default=20,
        type=int,
        help='Minimum MAPQ of reads. Default is 20.'
    )
    parser_command13.add_argument(
        '-w',
        '--workers',
        default=1,
        type=int,
        help='Number of subprocesses to use. Default is 1.'
    )
    # TODO: include what each level of verbosity entails.
    parser_command13.add_argument(
        '-v',
        '--verbose',
        default=0,
        action='count',
        help='Specify verbosity. Number of printed statements is proportional '
        'to number of vs.'
    )
    parser_command13.set_defaults(func=_cli_cleavage_profile)
    return parser


def main_cli():
    parser = main_cli_parser()

    args = parser.parse_args()
    function = args.func
    funcargs = vars(args)
    funcargs.pop('func')
    funcargs.pop('subcommand')

    function(**funcargs)


if __name__ == '__main__':
    main_cli()
