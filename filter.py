from tqdm import tqdm
import numpy as np

def num_lines_in_file(fname):
 
    with open(fname, 'r') as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

def filter_tsv_with_conf(
    input_file, output_file_lang_1, output_file_lang_2,
    confidence_threshold=None, confidence_column=None
):
  
    print()
    print('====================================')
    print('======= TSV Conf Filtering =========')
    print('====================================')
    print()
    num_lines = num_lines_in_file(input_file)
    scores = []
    num_output_lines = 0
    lang_1_col = 0
    lang_2_col = 1
    with open(input_file, 'r') as f, \
        open(output_file_lang_1, 'w') as f_out_1, \
        open(output_file_lang_2, 'w') as f_out_2:
        for line in tqdm(f, total=num_lines, desc=f"Filtering file by confidence {confidence_threshold}"):
            if line.strip() == '':
                continue
            line = line.strip().split('\t')
            if len(line) < 2:
                continue
            if confidence_threshold is not None and float(line[confidence_column]) < confidence_threshold:
                continue
            else:
                if confidence_threshold is not None:
                    scores.append(float(line[confidence_column]))
                    if confidence_column == 0:
                        lang_1_col, lang_2_col = 1, 2
                    elif confidence_column == 2:
                        lang_1_col, lang_2_col = 0, 1
                    elif confidence_column == 1:
                        lang_1_col, lang_2_col = 0, 2
                    else:
                        raise ValueError(f"Invalid Column for confidence {confidence_column}")
                f_out_1.write(line[lang_1_col] + '\n')
                f_out_2.write(line[lang_2_col] + '\n')
                num_output_lines += 1

    if confidence_threshold is not None:
        print(f'Confidence score average  : {np.mean(scores)}')
        print(f'Confidence score variance : {np.var(scores)}')
        print(f'Kept {num_output_lines} out of {num_lines} after conversion ({(num_output_lines / num_lines) * 100}%)')
        print('====================================')

filter_tsv_with_conf(
    'data/WikiMatrix.en-ru.tsv',
    'data/WikiMatrix.en-ru.en', 
    'data/WikiMatrix.en-ru.ru',
    confidence_threshold=1.04, confidence_column=0
)
