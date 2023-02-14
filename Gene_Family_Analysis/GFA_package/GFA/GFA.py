import requests
import pandas as pd
from typing import Optional
import os
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import logging
import sys

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class family:
    def __init__(self, gene: str = None, output_path:Optional[str] = None, map_orient: str = None, out_tree: str = None):
        self.gg_id= None
        self.geneids= None
        self.output_path= output_path
        self.gene= gene
        self.ref_id= None
        self.file_path=None
        self.out_tree = out_tree

        self.map_orient= map_orient
        if gene:
            self.fetch()

        if self.out_tree.endswith((".png", ".pdf", ".jpeg", ".svg", "jpg")):
            pass
        else:
            raise ValueError('Tree image must be either "pdf", "svg", "png", "jpg", "jpeg')
            logging.error('Wrong file format')

    def fetch(self) -> int:
        """to identify the gene group/family id """

        api_query = f"http://rest.genenames.org/fetch/symbol/{self.gene}"
        logging.info(' fetching gene file from HGNC....')
        response = requests.get(api_query, headers={"Accept": "application/json"})
        #if response != 200:
            #logging.warning('Try again with proper gene name')
        data= response.json()
        id= data['response']
        if id['numFound']==0:
            logger.warning('Gene not found in HGNC database')
            sys.exit()
        else:
            pass
        self.gg_id=id['docs'][0]['gene_group_id'][0]
        return self.gg_id
    #return (print(response))

    def main_frame(self):
        """To get a dataframe with required fields and values"""
        df = pd.read_csv('custom.txt', sep="\t")
        df['Gene group ID'] = df['Gene group ID'].str.split('|')
        new = df.explode('Gene group ID').reset_index(drop=True)
        df_new = new[new['Gene group ID'] == str(self.gg_id)]
        print(df_new)
        logging.warning('Nan values detected and dropped from list...')
        self.ref_id = df_new['RefSeq IDs'].dropna().tolist()
        return self.ref_id


    def fasta(self):
        """To gather sequences from RefSeq and make a .txt file in fasta format"""
        ref= self.main_frame()

        logging.info(' Inside fasta method....')

        ref_ids1 = ",".join(ref)
        api_query= f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={ref_ids1}&rettype=fasta&retmode=text"
        response = requests.get(api_query)
        data= response.text

        if os.path.exists(self.output_path):
            self.file_path= os.path.join(self.output_path,self.gene+'_family.txt')
            with open(self.file_path,'w') as f:
                f.write(data)
                f.close()
        return self.file_path

    def needleman_wunsch(self, seq1, seq2, match=1, mismatch=-1, gap=-2):
        """
        Perform global alignment of two sequences using the Needleman-Wunsch algorithm.
        :param seq1: The first sequence
        :param seq2: The second sequence
        :param match: The score for a match
        :param mismatch: The score for a mismatch
        :param gap: The score for a gap
        :return: Tuple of the aligned sequences and the alignment score
        """

        logging.debug(' Running the needleman wunsh....')

        # Initialize the scoring matrix
        rows = len(seq1) + 1
        cols = len(seq2) + 1
        score_matrix = [[0 for j in range(cols)] for i in range(rows)]

        # Initialize the traceback matrix
        traceback_matrix = [[0 for j in range(cols)] for i in range(rows)]

        # Fill in the first row and column of the matrices
        for i in range(1, rows):
            score_matrix[i][0] = score_matrix[i - 1][0] + gap
            traceback_matrix[i][0] = "up"
        for j in range(1, cols):
            score_matrix[0][j] = score_matrix[0][j - 1] + gap
            traceback_matrix[0][j] = "left"

        # Fill in the rest of the scoring matrix
        for i in range(1, rows):
            for j in range(1, cols):
                diagonal = score_matrix[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
                up = score_matrix[i - 1][j] + gap
                left = score_matrix[i][j - 1] + gap
                score_matrix[i][j], traceback_matrix[i][j] = max(
                    (diagonal, "diag"), (up, "up"), (left, "left"))

        # Traceback to find the aligned sequences
        align1, align2 = "", ""
        i, j = rows - 1, cols - 1
        while i > 0 and j > 0:
            if traceback_matrix[i][j] == "diag":
                align1 = seq1[i - 1] + align1
                align2 = seq2[j - 1] + align2
                i -= 1
                j -= 1
            elif traceback_matrix[i][j] == "up":
                align1 = seq1[i - 1] + align1
                align2 = "-" + align2
                i -= 1
            else:
                align1 = "-" + align1
                align2 = seq2[j - 1] + align2
                j -= 1

        # Add remaining characters in the beginning of the sequences
        while j > 0:
            align1 = "-" + align1
            align2 = seq2[j - 1] + align2
            j -= 1

        # Return the aligned sequences and the alignment score
        return align1, align2, score_matrix[rows - 1][cols - 1]

    def wrap_msa(self):
        """
        Wrapper function for MSA
        :param fasta_file: Fasta sequence obtained from API
        :return: List of list from which the phylogenetic tree can be made
        """
        new_path= self.fasta()
        with open(new_path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        sequence_list = []
        sequence = ""
        name=[]
        for line in content:
            if line.startswith(">"):
                name.append(line)
                if sequence:
                    sequence_list.append(sequence)
                    sequence = ""
            else:
                sequence += line
        if sequence:
            sequence_list.append(sequence)
        #print(name)
        listval = []
        for x in name:
            var = x.split('(')[1]
            tmp = var.split(')')[0]
            listval.append(tmp)
        print(listval)
        print(sequence_list)
        print(len(sequence_list))
        if len(listval)<5:
            logging.warning('Not enough sequences, should be more than 5')
            print("Not enough sequences, should be more than 5")
            sys.exit()

        elif len(listval)>15:
            logging.warning('Please upload less than 15 sequences')
            print("Please upload less than 15 sequences")
            sys.exit()
        else:
            pass

        ml = []
        sl = []
        for x in range(len(sequence_list)):
            for y in range(len(sequence_list)):
                align1, align2, score = self.needleman_wunsch(sequence_list[x], sequence_list[y])
                sl.append(score)
                y += 1
            x += 1
            ml.append(sl)
            sl = []
        return ml, listval


    def phylogeny(self):
        """Phylogeny tree for the retrieved sequences"""
        logging.info(' Phylogeny method....')

        scores , listval = self.wrap_msa()
        # Additional parameter for orientation
        # orientation = 'vertical' # or 'horizontal'

        # Perform linkage analysis on the scores
        linked = linkage(scores, method='ward')

        # Set the orientation to vertical/horizontal
        #orientation = input("Enter dendrogram orientation (vertical/horizontal): ")

        if self.map_orient not in ["v", "h"]:
            print("Invalid input, please enter either 'v' for vertical or 'h' for horizontal.")

        else:
            if self.map_orient == 'v':
                orientation = 'top'  # or 'bottom'
                dendrogram(linked, labels=listval, orientation= orientation)
                plt.savefig(self.out_tree)

            else:
                orientation = 'left'  # or 'right'
                dendrogram(linked, labels=listval, orientation= orientation)
                plt.savefig(self.out_tree)
