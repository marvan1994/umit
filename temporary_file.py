import pandas as pd

import json

import  os



allsubs = ['ang_ege', 'ang_oge', 'baz_ege', 'bio_ege', 'bio_oge', 'fiz_ege',
       'geo_ege', 'geo_oge', 'him_ege', 'him_oge', 'inf_ege', 'inf_oge',
       'ist_ege', 'ist_oge', 'lit_ege', 'lit_oge', 'mat_ege', 'mat_oge',
       'nem_ege', 'obs_ege', 'obs_oge', 'rus_oge', 'fiz_oge', 'ang_10c',
       'bio_10c', 'fiz_10c', 'him_10c', 'ist_10c', 'lit_10c', 'mat_10c',
       'obs_10c', 'rus_10c', 'rus_ege', 'inf_10c']


df = pd.read_csv('subtheme_sheet.csv')
df = df[['subject','class_year','section','subtheme','subtheme_id']].drop_duplicates()
df.class_year = df.class_year.map({3:'ege',1:'oge',4:'10c'})
df['sub_deg'] = df['subject']+'_'+df['class_year']


main_dict = dict(zip(allsubs, ['' for x in range(len(allsubs))]))

for sub_deg in allsubs:
    dft = df.query(f'sub_deg == "{sub_deg}"')
    sections = dft.section.unique().tolist()

    all_subtheme_names = dict(zip(dft.subtheme_id.tolist(),dft.subtheme.tolist()))
    sections_dict = { section: [str(int(x)) for x in dft.query(f'section == @section').subtheme_id.to_list()] for section in sections}

    subject_info = {'subtheme_names': all_subtheme_names, 'sections': sections_dict}

    main_dict[sub_deg] = subject_info

    with open(r'subtheme_info.json', 'w+') as f:

        json.dump(main_dict,f)

# for sub in all_subject_names:
#
#     df = pd.read_excel(f'.\\umit_files\\umit_{sub[0:3]}.xlsx')
#     print(sub)
#     N_sections = sum(1 for x in df.columns[0::2].to_list() if 'Unnamed' not in x)
#     section_names = df.columns[0:2 * N_sections:2]
#     id_columns = df.columns[1:2 * N_sections:2]
#     umit_ids = []
#     umit_names = []
#     for x in range(N_sections):
#         umit_names.extend(df[section_names[x]].dropna().to_list())
#         section_ids = [str(int(x)) for x in df[id_columns[x]].dropna().to_list()]
#         umit_ids.extend(section_ids)
#     all_umit_names = dict(zip(umit_ids, umit_names))
#
#     sections = {section_names[x]: [str(int(x)) for x in df[id_columns[x]].dropna().to_list()] for x in
#                 range(N_sections)}
#
#     subject_info = {'umit_names': all_umit_names, 'sections': sections}
#
#     subject_name = sub
#     main_dict[subject_name] = subject_info
#
# with open('umit_info.json', 'w+') as f:
#     json.dump(main_dict, f)
#
#
#
