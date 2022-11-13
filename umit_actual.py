import json

import pandas as pd

from pathlib import Path

#creating all basic files

all_subject_names = ['ang_ege', 'baz_ege', 'bio_ege', 'geo_ege', 'inf_ege', 'ist_ege', 'lit_ege', 'mat_ege',
                         'nem_ege', 'rus_ege', 'fiz_ege', 'him_ege', 'obs_ege']
        

path = Path('.')

def main_umit_info_add(subject_info, subject_name):

    with open(r'umit_info_spec.json', 'r') as f:

        main_dict = json.loads(f.read())

        main_dict[subject_name] =  subject_info

    with open(r'umit_info_spec.json', 'w+') as f:

        json.dump(main_dict,f)


def umit_info_actualisation():

    path = Path('umit_files')


    for file in path.iterdir():
    
        sub = file.name[5:-5]

        df = pd.read_excel(file)
        N_sections = sum(1 for x in df.columns[0::2].to_list() if 'Unnamed' not in x)
        section_names = df.columns[0:2*N_sections:2]
        id_columns = df.columns[1:2*N_sections:2]
        umit_ids = []
        umit_names = []
        for x in range(N_sections):
            umit_names.extend(df[section_names[x]].dropna().to_list())
            section_ids = [str(int(x)) for x in df[id_columns[x]].dropna().to_list()]
            umit_ids.extend(section_ids)
        if len(umit_names) == len(umit_ids):
            all_umit_names = dict(zip(umit_ids,umit_names))

            sections = {section_names[x]:[str(int(x)) for x in df[id_columns[x]].dropna().to_list()] for x in range(N_sections)}

            subject_info = {'umit_names':all_umit_names, 'sections':sections}

            main_umit_info_add(subject_info, sub)
        else:
            print(f'check umits {sub}. In one of the sections length of umit_names and umit_ids doesnt equal.')
                   
umit_info_actualisation()