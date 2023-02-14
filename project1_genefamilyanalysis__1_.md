# Programming Project 01 - Gene Family Analysis

## Group Projects
These projects serve as a way for you to learn how to build a programmatic tool in a group setting. Often in this field, large packages and software are built in a collaborative effort, and knowing how to effectively communicate ideas, tasks, and workflow is an essential skill. Here, you will work as part of a group and demonstrate your ability to compose a cohesive (and working) tool comprised of components created by others *and* yourself.

## Deadline
**February 07, 2023 - 12:00/noon (UTC+1:00)**

## Submission Guidelines
1. Clone your repository to your local workstation/computer if you have not done so
2. Structure and work on your submission.
3. Commit your work to the git repository.
4. Create a git tag.
  * Tag name must be equivalent to ”GroupProject”.
  * Tag can be made via the command line or using the GitLab GUI
5. Be sure to include a PDF of your presentation in your repository once it is finished

## Package Requirements
* All code comprising the backend portion (i.e. the code responsible for downloading, parsing, and formatting the information) must be compiled as an installable Python package
* The package must contain the following:
    * A working CLI (see [CLI Requirements](#cli-requirements) below)
    * A clear and descriptive `README.md` that details what the package is, what it does, how it can be used, and examples of how to use the CLI
    * The necessary dependencies so that the package works immediately upon installation in a new virtual environment
    * Working unit tests that test at least 70% of the code in the package

## CLI Requirements
* Within your python package there must also be a working command line interface (CLI)
* CLI methods must contain proper documentation that is accessible via the command line
* CLI method documentation should contain:
    * Explanations of the arguments and options involved with the method
    * Brief description of what the method is used for

## Use of External Libraries
In general, one can make use of an external library or package that can aid in accomplishing a small subtask, such as a combinatorial problem, interface with an API, etc., but you cannot use a library or package capable of solving __all__ of your tasks. You are of course allowed to use modified code from your previous individual assignments (including that of PLAB1) where applicable. If you do choose to use an external resource to perform part of one of your tasks, it must be properly explained in the presentation. If you have any questions or concerns about whether a particular resource is allowed, please feel free to ask via email or issue.

## General Remarks
* The tasks are purposely written in such as manner as to require you, as a group, to figure out what tools are needed, what information needs to be gathered, and what resources should be used
* All code-based work is to be done in GitLab
* Use GitLab Issues to track and assign individual tasks and required work
* The software package (backend code) and web application (frontend) can be stored in separate folders in the root directory of your repository as shown here (you can rename these folders as you please):
```bash
├── frontend
└── project_package
```

## Grading (10 pts):

| Task | 1 | 2 | 3 | 4 | 5 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Points | 2 | 2 | 2 | 3 | 1 |

<div style="page-break-after: always"></div>

## Gene Family Analysis - Introduction
Gene families occur often in nature due to a duplication event in a specific gene which results in multiple instances of similar strands of genetic code that produce proteins with very similar biochemical functions. A few popular examples of gene families include the immunoglobulin superfamily (IgA, IgM, IgE, etc), MAP kinases, and G-proteins. Because gene families often are derived from a single progenitor gene, the genetic sequence of its members is typically conserved allowing one to identify its members through alignment and to construct a __phylogeny__ or __phylogenetic tree__.  

A phylogenetic tree is a visual representation of how a group of biological entities (species, organisms, genes, etc.) may have been derived over time (see Figure 1). Because describing at what point in the evolutionary timeline a gene or species may have diverged, it is typically much more helpful to create such a figure to visually depict how everything is related. Gene families can also serve as an indicator how closely related two species are, and therefore a helpful tool for a biologist would be one that can quickly generate a phylogeny for a given gene family.


![](img/p01_phylogeny.jpg)
__Figure 1__: Example of a phylogenetic tree for several species.


## Aims
The task for this project to build a pipeline that can generate a DNA-based phylogenetic tree for a given gene family. Your software package should do the following:
1. __Find the members of a given gene family__ and download their genetic sequences
2. __Align the genetic sequences__ of the gene family members. This may require the use of insertions/deletions (indels) and multiple sequence alignment
3. __Score the alignments__ using a established technique or algorithm
4. __Construct a phylogenetic tree__ of the gene family and be able to export said image in a variety of formats
5. __Create a frontend__ that allows one to provide a gene family term and visualize its corresponding phylogenetic tree

## Tasks

### Task 1 - *Finding Out Who is in the Family* (2 pts)
* Gene families (or gene groups) are classified by [HGNC](https://www.genenames.org/data/genegroup/#!/). Develop a strategy to use the information available in HGNC to determine the members of a given gene family
* Once the members are determined, you will need to extract their genetic sequences. The generally accepted "standard" genetic sequence for a gene can be found using [RefSeq](https://www.ncbi.nlm.nih.gov/refseq/about/)

### Task 2 - *Align and Score* (2 pts)
* Create a series of methods that align the sequences of the gene family members and score them based on their similarity. To do this, you will need to perform a multiple sequence alignment

### Task 3 - *Build the Tree* (2 pts)
* Using an established technique or algorithm, compile a phylogenetic tree based on the alignment scores generated in Task 2
* Allow one to be able to export the generated phylogenetic tree in several formats including png, jpg, svg, and pdf

### Task 4 - *GUI* (3 pts)
* Construct a web interface that allows one to provide a gene family/group term and visualize the resulting phylogenetic tree. Your interface should include the following features:
    * A text box + submit button for inputting the gene family/group term
    * A table of the gene family/group members and an expandable button to visualize their genetic sequences
    * A matrix of alignment scores for every combination of the gene family/group members
    * An area depicting the resulting phylogenetic tree image
    * The ability for one to choose which file format to download the phylogenetic tree image

### Task 5 - *Containerize the Application* (1 pt)
* Create a `Dockerfile` in your project's root directory that successfully compiles your application into a Docker image
    * It should bundle your backend and frontend code together
    * You may choose any base image
    * All members of group should be in the image metadata using `LABEL`
    * The `ENTRYPOINT` should start your web application and the web app should be accessible using port mappings


## Hints
* [Genomes](https://www.ncbi.nlm.nih.gov/books/NBK21122/) has a great chapter on this subject
