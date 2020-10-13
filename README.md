<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contact](#contact)


<!-- ABOUT THE PROJECT -->
## About The Project

This project contains the code for the assignments of CS2220, Introduction to Computational Biology.

In assignment 1, we use the RNA sequenced data, in the form of fasta files, and use it to predict the translation initiation sites of mRNA.

In assignment 2, we use the data from the Affymetrix GeneChip, which shows us the levels of the gene expression, and use it for childhood acute lymphoblastic leukemia subtype diagnosis. 

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Datasets required to run this code in contained in this repo


### Installation

1. Clone the repo
```sh
git clone https://github.com/ChewKinWhye/CS2220.git
```
2. Create venv
```sh
cd CS2220
python3 -m venv CS2220_env
source CS2220_env/bin/activate 
```
3. Install requirements
```sh
pip install -U pip
pip install -r requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

Assignment 1

```sh
python assignment_1.py
```
Assignment 2

```sh
python assignment_2.py
```

<!-- CONTACT -->
## Contact

Chew Kin Whye - kinwhyechew@gmail.com
