import pandas as pd
import os
import numpy as np
import csv


def count_ALL_subtype(label_file):
    df = pd.read_excel(label_file)
    count = 0
    for _, row in df.iterrows():
        if row['Coding'] == "T-ALL":
            count += 1
    return count


def count_genes(file_path):
    gene_files_count = []
    for file in os.listdir(file_path):
        # Only open txt files
        if file[-4:].lower() != ".txt":
            continue
        with open(os.path.join(file_path, file)) as f:
            gene_count = 0
            for row in f:
                row_array = row.split("\t")
                if row_array[0][-3:] == "_at":
                    gene_count += 1
        gene_files_count.append(gene_count)
    return gene_files_count


def common_genes(file_path):
    common_genes_set = None
    for file in os.listdir(file_path):
        if file[-4:].lower() != ".txt":
            continue
        gene_set = set()
        with open(os.path.join(file_path, file)) as f:
            for row in f:
                row_array = row.split("\t")
                # row_array[0] is the name, and row_array[5] is the presence/absence of the gene
                if row_array[0][-3:] == "_at" and row_array[0][0:4].upper() != "AFFX" and row_array[5].upper() == "P":
                    gene_set.add(row_array[0])
        # Initialise common gene set
        if common_genes_set is None:
            common_genes_set = gene_set
        # Get the intersection
        else:
            common_genes_set = common_genes_set.intersection(gene_set)
    return common_genes_set


def clean_and_merge(file_path_data, file_path_label, common_genes, output_filename):
    output_data = []
    output_data.append(common_genes + ["Label"])
    labels = pd.read_excel(file_path_label)
    for file in os.listdir(file_path_data):
        if file[-4:].lower() != ".txt":
            continue
        output_row = np.zeros((len(common_genes)))
        with open(os.path.join(file_path_data, file)) as f:
            for row in f:
                row_array = row.split("\t")
                if row_array[0] in common_genes:
                    idx = common_genes.index(row_array[0])
                    output_row[idx] = row_array[4]
        output_row = list(output_row)
        row_label = list(labels.loc[labels["Chip"] == file[:-4]]["Coding"])
        row_label = [1 if label == "T-ALL" else 0 for label in row_label]
        output_data.append(output_row + row_label)
    with open(output_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output_data)
    output_data = np.array(output_data)
    return output_data[1:, :-1].astype(np.float), output_data[1:, -1].astype(np.float)
