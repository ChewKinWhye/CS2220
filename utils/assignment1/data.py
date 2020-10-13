import numpy as np


def load_fast_data(fast_filename):
    dna_lookup = {'A': [1], 'T': [2],
                  'G': [3], 'C': [4], 'N': [5]}
    data_x = []
    with open(fast_filename) as f:
        for idx, line in enumerate(f):
            row_data = []
            if idx % 2 == 0 or line.find("X") != -1:
                continue

            for x in line[:-1]:
                row_data.extend(dna_lookup[x])
            data_x.append(row_data)
    data_x = np.asarray(data_x)

    if fast_filename.find("pos") != -1:
        data_y = np.ones(data_x.shape[0])
    else:
        data_y = np.zeros(data_x.shape[0])
    return np.asarray(data_x), data_y


def raw_to_pos_fast(raw_file="Dataset/Assignment1/vertebrates.txt"):
    # Initialize empty lists
    dna_data_point, label_data_point = [], []
    total_dna_data, total_label_data = [], []
    end, to_read_dna = False, False
    with open(raw_file) as f:
        to_read_dna = False
        for row in f:
            # Split row by empty spaces
            row_split = row.split()
            # Ignore the row containing the metadata (Always starts with numbers)
            if row_split[0].isnumeric():
                # DNA data is right after metadata
                to_read_dna = True
                end = False
                # Reinitialise with empty list
                dna_data_point = []
                label_data_point = []
                continue
            elif to_read_dna:
                dna_data_point.extend(row_split[0])
                if len(row_split) == 1:
                    # If the length is 1, there is no more DNA data in this section
                    to_read_dna = False
            else:
                label_data_point.extend(row_split[0])
                if len(row_split) == 1:
                    # If the length is 1, there is no more label data in this section
                    end = True
            if end:
                total_dna_data.append(dna_data_point)
                total_label_data.append(label_data_point)
    # Now each data point is represented as a row in total_dna_data and total_label_data
    # We have to use this to create the pos fast data
    pos_fast_data = []
    for i in range(len(total_dna_data)):
        pos_fast_data_point = []
        # Position of A in ATG
        idx = total_label_data[i].index('i')
        # Check if front padding if needed
        if idx < 99:
            # Append the padding
            for _ in range(99-idx):
                pos_fast_data_point.append("N")
            # Add the DNA data up till and including the A
            pos_fast_data_point.extend(total_dna_data[i][0:idx+1])
        else:
            # If front padding not needed, we can append the 100 letters in front of T
            pos_fast_data_point.extend(total_dna_data[i][idx-99:idx+1])

        # Check if back padding if needed
        if len(total_dna_data[i]) < idx + 102:
            # Add the DNA data from the T all the way to the end
            pos_fast_data_point.extend(total_dna_data[i][idx+1:])
            # Add the back padding
            for _ in range(idx + 102 - len(total_dna_data[i])):
                pos_fast_data_point.append("N")
        else:
            # If back padding is not needed, we can append T and the 100 letters behind it
            pos_fast_data_point.extend(total_dna_data[i][idx + 1:idx + 102])
        # Convert list of characters to a string
        pos_fast_data_point = ''.join(pos_fast_data_point)
        pos_fast_data.append(pos_fast_data_point)
    return pos_fast_data


def raw_to_neg_fast(raw_file="Dataset/Assignment1/vertebrates.txt"):
    # Initialize empty lists
    dna_data_point, label_data_point = [], []
    total_dna_data, total_label_data = [], []
    end, to_read_dna = False, False
    with open(raw_file) as f:
        to_read_dna = False
        for row in f:
            # Split row by empty spaces
            row_split = row.split()
            # Ignore the row containing the metadata (Always starts with numbers)
            if row_split[0].isnumeric():
                # DNA data is right after metadata
                to_read_dna = True
                end = False
                # Reinitialise with empty list
                dna_data_point = []
                label_data_point = []
                continue
            elif to_read_dna:
                dna_data_point.extend(row_split[0])
                if len(row_split) == 1:
                    # If the length is 1, there is no more DNA data in this section
                    to_read_dna = False
            else:
                label_data_point.extend(row_split[0])
                if len(row_split) == 1:
                    # If the length is 1, there is no more label data in this section
                    end = True
            if end:
                total_dna_data.append(dna_data_point)
                total_label_data.append(label_data_point)
    # Now each data point is represented as a row in total_dna_data and total_label_data
    # We have to use this to create the neg fast data
    neg_fast_data = []
    for i in range(len(total_dna_data)):
        for idx in range(len(total_dna_data[i])-2):
            neg_fast_data_point = []
            # Check for ATG and check that the index is not the index of a positive example
            if total_dna_data[i][idx] == "A" and total_dna_data[i][idx+1] == "T" \
                and total_dna_data[i][idx+2] == "G" and idx != total_label_data[i].index('i'):
                if idx < 99:
                    # Append the padding
                    for _ in range(99 - idx):
                        neg_fast_data_point.append("N")
                    # Add the DNA data up till and including the A
                    neg_fast_data_point.extend(total_dna_data[i][0:idx + 1])
                else:
                    # If front padding not needed, we can append the 100 letters in front of T
                    neg_fast_data_point.extend(total_dna_data[i][idx - 99:idx + 1])

                # Check if back padding if needed
                if len(total_dna_data[i]) < idx + 102:
                    # Add the DNA data from the T all the way to the end
                    neg_fast_data_point.extend(total_dna_data[i][idx + 1:])
                    # Add the back padding
                    for _ in range(idx + 102 - len(total_dna_data[i])):
                        neg_fast_data_point.append("N")
                else:
                    # If back padding is not needed, we can append T and the 100 letters behind it
                    neg_fast_data_point.extend(total_dna_data[i][idx + 1:idx + 102])
                # Convert list of characters to a string
                neg_fast_data_point = ''.join(neg_fast_data_point)
                neg_fast_data.append(neg_fast_data_point)
    return neg_fast_data


def in_frame_three_gram(row):
    # Row contains 99 values, code can be reused for up or down stream
    nucleotides = ['A', 'T', 'G', 'C']
    three_grams = []
    for i in nucleotides:
        for ii in nucleotides:
            for iii in nucleotides:
                three_gram = i + ii + iii
                three_grams.append(three_gram)
    # three_grams now contains 4^3 values, AAA to CCC
    # Initialise count with zeros
    three_grams_count = [0] * 4**3
    for idx in range(0, len(row), 3):
        three_gram = row[idx] + row[idx+1] + row[idx+2]
        # Position will be 0 for AAA, 1 for AAT ... 63 for CCC
        try:
            position = three_grams.index(three_gram)
            three_grams_count[position] += 1
        except:
            # three gram contains "N", ignore
            pass
    # Sum of all the values in three_grams_count will be 99/3 = 33, if no "N"s
    return three_grams_count


def in_frame_three_gram_up_and_down(row):
    # Row contains 201 values
    upstream_in_frame_three_gram = in_frame_three_gram(row[0:99])
    downstream_in_frame_three_gram = in_frame_three_gram(row[101:])
    return upstream_in_frame_three_gram, downstream_in_frame_three_gram


def extract_arff_data(filepath="Dataset/Assignment1/Inframe_3_Gram.arff"):
    x = []
    y = []
    with open(filepath) as f:
        for line in f:
            if line[0] == "@" or line[0] == "\n":
                continue
            data = line.split(",")
            x.append([int(i) for i in data[0:-1]])
            y.append(1 if data[-1] == "pos\n" or data[-1] == "pos" else 0)
    return np.asarray(x), np.asarray(y)


