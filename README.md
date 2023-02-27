# Gene Family Analysis
***
The Gene Family Analysis is a GUI, CLI inclusive package for analysing the Gene families with the help of Multiple Sequence alignment and Phylogenetic Tree construction. 

[Gene Families](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2683547/) are widely used in comparative genomics, molecular evolution, and in systematics. However, they are constructed in different manners, their data analyzed and interpreted differently, with different underlying assumptions, leading to sometimes divergent conclusions. In systematics, concepts like monophyly and the dichotomy between homoplasy and homology have been central to the analysis of phylogenies.

The package allows user to build a phylogenetic tree in their preferred location on their machine along with whether the tree they want is horizontal or vertical along with the format of the output image.
***
### Method

GFA will fetch all members of the gene family by providing it with an HGNC gene ID. Once it has fetched the information and sequences from HGNC API, It will check if there are NaN values present for the sequences. Afterwards it will perform a Multiple sequence alignment using the standard Needleman-wunsch algorithm for the global alignment with all the included sequences and will generate a score based on the distance in their evolutionary relationship. The generated scores will then be used to create a phylogtenetic tree which provides the information of how closely or distantly related are the sequences from each other even though being in the same gene family.

## Getting Started

To be abel to run this package on your machine you will have to install the package on your local machine.
***

### Prerequisites

Requirements for the software (Required python packages).
-  Click
-  matplotlib
-  pandas
-  requests
-  scipy
-  Pillow
-  pathlib
-  flask
-  typing
-  os
-  logging 
-  sys
***
### Installing

For installing the package you will have to run this command on your preferred IDE terminal

    pip install <location>GFA_package/
***
### Application

Tfe user can use the in-built cli by using the tree command like this:

    GFA tree [HGNC Gene ID] [preferred path for downloading] [h/v] [image format]
***
## Example

    GFA tree HBB -f localhost -o h -i localhost/pdf

The command written above should provide you with the tree present in the PDF format
***
## url for frontend

     Running on http://127.0.0.1:5000
If the link does not appear in the terminal after running the run.py file, the above link can be used to access it.
***

## Authors

  - **Ruchi Tanavade** 
  - **Anna Askenova** 
  - **Anoop Johny** 
  - **Harshnad Maru** 
***

#The project is not completed yet. Unittests and containerization remaining.

#### splendorous-churros-9b4b6b.netlify.app

#### https://sweet-sopapillas-08f1e5.netlify.app/
