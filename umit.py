import streamlit as st

import pandas as pd

import json

from load_css import local_css

import pathlib

path_umit = pathlib.Path.cwd() / 'umit_files'

st.set_page_config(page_title='Привязка умитов',
    page_icon="um.ico",)

local_css("style.css")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

all_subject_names = ['ang_ege', 'baz_ege', 'bio_ege', 'geo_ege', 'inf_ege', 'ist_ege', 'lit_ege', 'mat_ege',
                         'nem_ege', 'rus_ege', 'fiz_ege', 'him_ege', 'obs_ege']
#umit_actual.umit_info_actualisation(all_subject_names)


def reset_session():
    st.session_state.umit = []


def show():

    st.sidebar.image('um.png', caption=None, width = 100, use_column_width='True', clamp=False, channels="RGB", output_format="auto")


    st.write(
        """
        ## Это программа для привязывания умитов
        """
    )


    def umit_add(subject_name,subject_info,rec_umits):

        #rec = st.checkbox('Показывать только рекомендованные умиты')
        rec = False
        sub = subject_name[0:3]
        #recomended = rec_umits[subject_name].split(',')
        recomended = []
        # if rec == True:
        #     st.markdown(recomended)

        df = pd.read_excel(path_umit/ pathlib.Path('umit_'+sub+'.xlsx'), dtype = str)
        df.fillna('', inplace=True)
        st.dataframe(df)

        if 'umit' not in st.session_state:
             st.session_state.umit = []

        #subject_name = 'rus_ege'

        # column_names = list(df.columns)
        # section_names = [name for name in column_names if 'Unnamed' not in name]
        #
        # umit_columns = [column_names[column_names.index(section)+1] for section in section_names]

        section_names = list(subject_info['sections'].keys())
        section = st.selectbox(label = 'Выберите раздел', options = ['']+section_names , key = subject_name)

        if section !='':

            #subdf = df[[section,umit_columns[section_names.index(section)]]].dropna()

            #st.dataframe(subdf)

            umit_number_to_name = {key: subject_info['umit_names'][key] for key in subject_info['umit_names'].keys()}
            umit_name_to_number = {value: key for (key, value) in umit_number_to_name.items()}


            section_number_list = subject_info['sections'][section]

            if rec == True:
                section_number_list = [num for num in section_number_list if num in recomended]


            section_name_list = [umit_number_to_name[umit] for umit in section_number_list]

            for i in range(len(section_number_list)):

                if int(section_number_list[i]) in st.session_state.umit:

                    cheker = st.checkbox(f'{section_name_list[i]} ({int(section_number_list[i])})', key = subject_name+'_'+str(section_number_list[i]), value= True)

                else:
                    cheker = st.checkbox(f'{section_name_list[i]} ({int(section_number_list[i])})', key = subject_name+'_'+str(section_number_list[i]))


                if cheker:

                    current_state = list(set(st.session_state.umit))
                    current_state.extend([int(section_number_list[i])])
                    current_state = list(set(current_state))
                    st.session_state.umit = current_state

                else:
                    current_state = list(set(st.session_state.umit))

                    if int(section_number_list[i]) in st.session_state.umit:
                        current_state = st.session_state.umit
                        current_state.remove(int(section_number_list[i]))
                        st.session_state.umit = current_state



                #st.checkbox(f'{umit} ({df[umit_columns[section_names.index(section)], section]})')

    with open('umit_info_spec.json', 'r') as f:
        umit_info = json.loads(f.read())
    with open('recomended_umits.json', 'r') as f:
        rec_umits = json.loads(f.read())

    subjects_inrus = ['Английский', "Базовая", "Биология", "География", "Информатика", "История", "Литература",
                      "Математика", "Немецкий", "Русский", "Физика", "Химия", 'Обществознание']
    subjects_ineng = ['ang', 'baz', 'bio', 'geo', 'inf', 'ist', 'lit', 'mat', 'nem', 'rus', 'fiz', 'him', 'obs']
    subject_names_ege = ['ang_ege', 'baz_ege', 'bio_ege', 'geo_ege', 'inf_ege', 'ist_ege', 'lit_ege', 'mat_ege',
                         'nem_ege', 'rus_ege', 'fiz_ege', 'him_ege', 'obs_ege']
    subject_dict = dict(zip(subjects_inrus, subjects_ineng))
    #subject_dict = {'Английский': 'ang', 'Математика': 'mat', 'Обществознание': 'obs'}

    subject_names = umit_info.keys()

    subject = st.sidebar.selectbox('Выберите предмет', [''] + list(subject_dict.keys()))
    #degree = st.sidebar.radio('Выберите направление', ['ЕГЭ', 'ОГЭ'])
    degree = ''
    degree_dict = {'ЕГЭ': 'ege', 'ОГЭ': 'oge'}

    try:
        subject_name = subject_dict[subject]
        if subject_name in subject_names:

            st.markdown(f'##### Умиты по предмету {subject} {degree}')

            subject_info = umit_info[subject_name]
            umit_add(subject_name, subject_info,rec_umits)

        else:

            st.markdown(f'##### Умитов по направлению {degree} по предмету {subject} не существует')

    except KeyError:
        pass

    show_umit()
def show_umit():

    t1 = st.sidebar.empty()
    t1.markdown('# Здесь будут отображаться умиты')
    if 'umit' in st.session_state:

        current_state = st.session_state.umit

        if len(current_state) !=0:

            current_state.sort()
            current_state_str = [str(item) for item in current_state]
            t1.text_area(label = 'Умиты можно копировать отсюда',value=','.join(current_state_str))
            istrue = st.sidebar.button('Очистить умиты')
            if istrue:
                reset_session()
                current_state_str = [str(item) for item in st.session_state.umit]
                t1.markdown(','.join(current_state_str))


show()


