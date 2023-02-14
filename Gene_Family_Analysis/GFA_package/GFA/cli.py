import click
from GFA import family
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@click.group()
def main():
    pass

@main.command()
@click.argument('gene_sym')
@click.option('-f','--fasta_output', help='Output path')
@click.option('-o','--orientation', help= 'Orientation (v/h)')
@click.option('-i','--image_output', help ='Preferred output format and path' )

def tree(gene_sym: str, fasta_output: str, orientation: str, image_output: str ):
    """
    This Command will generate a phylogenetic tree with preferred Gene ID, Orientation and output path on a local machine.
    [ARG 1] : Gene ID
    [ARG 2] : Output path
    [ARG 3] : Orientation (v/h)
    [ARG 4] : Preferred output format and path
    """
    alignment = family(gene = gene_sym, output_path = fasta_output, map_orient = orientation , out_tree=image_output)
    alignment.phylogeny()

if __name__ == "__main__":
    main()