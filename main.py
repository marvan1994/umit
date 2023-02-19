import pandas as pd

import json

import  os



speakers = ['Артур Шарафиев', 'Анастасия Малова', 'Александр Долгих',
       'Аля Виноградова', 'Фариша Князева', 'Аделия Адамова',
       'Жанна Казанская', 'Виктория Ларионова', 'Макс Тесла',
       'Надежда Ковалевская', 'Милена Соколова', 'Виктория Ланская',
       'Анастасия Майер', 'Семён Кравченко', 'Максим Кораблёв',
       'Елена Зеленская', 'Дарья Королёва', 'Ольга Чехова',
       'Александра Лебедева', 'Алина Вернадская', 'Андрей Баканчев',
       'Данир Баев', 'Богдан Чагин', 'Равиль Кандинский', 'Азат Антипов',
       'Вероника Соколовская', 'Дарья Львова', 'Анастасия Гласная',
       'Денис Марков', 'Артем Фролов', 'Алина Максимова', 'Никита Павлов',
       'Лина Клевер', 'Шерин Келли', 'Айнур Даллас', 'Айбулат Чева',
       'Кристина Лазарева', 'Александра Май', 'Кристина Мельникова',
       'Никита Сахаров', 'Татьяна Граева', 'Никита Равич',
       'Елизавета Островская', 'Евгений Тьюринг', 'Илья Кузьмин',
       'Мария Вельф', 'Анастасия Аддамс', 'Софья Вайб']


df = pd.read_csv('subtheme_import_v2.csv').rename(columns = {'Спикер':'speaker', 'Раздел':'section', 'Подтема':'subtheme','Айди подтемы':'subtheme_id'})
df = df[['speaker','section','subtheme','subtheme_id']].drop_duplicates()

main_dict = dict(zip(speakers, ['' for x in range(len(speakers))]))

for speak in speakers:
    dft = df.query(f'speaker == "{speak}"')
    sections = dft.section.unique().tolist()

    all_subtheme_names = dict(zip(dft.subtheme_id.tolist(),dft.subtheme.tolist()))
    sections_dict = { section: [str(int(x)) for x in dft.query(f'section == @section').subtheme_id.to_list()] for section in sections}

    subject_info = {'subtheme_names': all_subtheme_names, 'sections': sections_dict}

    main_dict[speak] = subject_info

    with open(r'subtheme_info_v2.json', 'w+') as f:

        json.dump(main_dict,f)


#
#
