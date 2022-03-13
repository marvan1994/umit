import pandas as pd

import json

import  os

path_to_umit_files = '.\\umit_files\\'

subjects_inrus = ['Английский', "Базовая", "Биология", "География", "Информатика", "История", "Литература", "Математика", "Немецкий", "Русский", "Физика", "Химия",'Обществознание']
subjects_ineng = ['ang','baz','bio','geo','inf','ist','lit','mat','nem','rus','fiz','him','obs']
subject_names_ege = ['ang_ege','baz_ege','bio_ege','geo_ege','inf_ege','ist_ege','lit_ege','mat_ege','nem_ege','rus_ege','fiz_ege','him_ege','obs_ege']
subject_names_oge = ['ang_oge','bio_oge','geo_oge','inf_oge','ist_oge','lit_oge','mat_oge','nem_oge','rus_oge','fiz_oge','him_oge','obs_oge']

subject_names_r2e = dict(zip(subjects_inrus,subjects_ineng))
subject_names_e2r = dict(zip(subjects_ineng,subjects_inrus))

all_subject_names = subject_names_ege + subject_names_oge


main_dict = dict(zip(all_subject_names, ['' for x in range(len(all_subject_names))]))

list_dir = os.listdir(path_to_umit_files)

for sub in all_subject_names:

    df = pd.read_excel(f'.\\umit_files\\umit_{sub[0:3]}.xlsx')
    print(sub)
    N_sections = sum(1 for x in df.columns[0::2].to_list() if 'Unnamed' not in x)
    section_names = df.columns[0:2 * N_sections:2]
    id_columns = df.columns[1:2 * N_sections:2]
    umit_ids = []
    umit_names = []
    for x in range(N_sections):
        umit_names.extend(df[section_names[x]].dropna().to_list())
        section_ids = [str(int(x)) for x in df[id_columns[x]].dropna().to_list()]
        umit_ids.extend(section_ids)
    all_umit_names = dict(zip(umit_ids, umit_names))

    sections = {section_names[x]: [str(int(x)) for x in df[id_columns[x]].dropna().to_list()] for x in
                range(N_sections)}

    subject_info = {'umit_names': all_umit_names, 'sections': sections}

    subject_name = sub
    main_dict[subject_name] = subject_info

with open('umit_info.json', 'w+') as f:
    json.dump(main_dict, f)



