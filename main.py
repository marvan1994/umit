import pandas as pd

import streamlit as st

import plotly.express as px

import os

import json

from PIL import Image

from load_css import local_css

st.set_page_config(page_title='Уровни знаний')

local_css("style.css")


def text_in_orange_highlight(text):
    return "<div align = \"middle\"> <span class='highlight orange'> {0} </span><div>".format(text)


def text_in_red_color(text):
    return "<h1 style = \"font-size: 12px; color: #800000\"> {0} </h1>".format(text)


def text_for_section(text):
    return "<pre style = \"font-size: 22px; color: #E3963E\"> {0}  </pre>".format(text)


def text_for_theme(text):
    return "<pre style = \"font-size: 14px; color: #7A3803\"> {0} </pre>".format('\t\t' + text)


def result_view(stud_info, subject_name, only_nulls):
    results = stud_info['subjects'][subject_name]

    sections = stud_info['subjects'][subject_name]['sections'].keys()

    for section in sections:
        section_knowledge = stud_info['subjects'][subject_name]['sections'][section]['knowledge']

        st.markdown(
            text_for_section(section.replace('\n', '') + '\t' + str(round(float(section_knowledge) * 100, 1)) + ' %'),
            unsafe_allow_html=True)

        themes = stud_info['subjects'][subject_name]['sections'][section]['themes'].keys()

        for theme in themes:
            theme_knowledge = stud_info['subjects'][subject_name]['sections'][section]['themes'][theme]['knowledge']

            if only_nulls == False:
                st.markdown(
                    text_for_theme(theme.replace('\n', '') + '\t' + str(round(float(theme_knowledge) * 100, 1)) + ' %'),
                    unsafe_allow_html=True)
            elif float(theme_knowledge) == 0:
                st.markdown(
                    text_for_theme(theme.replace('\n', '') + '\t' + str(round(float(theme_knowledge) * 100, 1)) + ' %'),
                    unsafe_allow_html=True)

def get_stud_info(stud_id, subject_name, only_nulls = False):

    students = os.listdir('.\\stud_info')

    stud_id = f'stud_{stud_id}_info.json'



    if len(stud_id)>3:

        if stud_id not in students:

            st.markdown(text_in_red_color('Результаты идеального ученика для этого преподавателя ещё не посчитаны... '), unsafe_allow_html=True)
        else:


            with open('.\\stud_info\\' + stud_id, 'r+') as f:

                stud_info = json.loads(f.read())
                result_view(stud_info, subject_name,only_nulls)

df = pd.read_excel('all_preps.xlsx')

prep_names = [name.upper() for name in df['Преподаватель'].values.tolist()]
prep_ident = df['Идентефикатор'].values.tolist()
prep_subject = df['Класс'].values.tolist()
teacher_dict = {prep_names[i]: prep_subject[i]+'_'+prep_ident[i]+'_best' for i in range(len(df))}
st.markdown(text_in_orange_highlight('Исскуственный интеллект от Умскул.  Страница для преподавателей'), unsafe_allow_html=True)
st.markdown('\n')
st.markdown('\n')
st.markdown('###### На этом сайте можно посмотреть как на искусственный интеллект '
            'оценивает понимание разделов и тем, которые мог бы пройти \"идеальный ученик\" '
            ' по итогу изучения программы с сентября по ноябрь. Считается, что такой ученик решал '
            'все домашние задания, причём исключительно на максимальный балл.')
st.markdown('______________________________________________________________________________')

input_name = st.sidebar.text_input('ИМЯ преподавателя' , key = 'input_name')
input_last = st.sidebar.text_input('ФАМИЛИЯ преподавателя' , key = 'input_last')

if len(input_name) <1 and len(input_last) <1:
    st.text('...где-то тут будут результаты...')

else:

    try:
        teacher_name = input_name.replace(' ','').upper()+' '+input_last.replace(' ','').upper()
        stud_id = teacher_dict[teacher_name]
        subject_name = stud_id[0:7]

        if len(stud_id.replace(' ', '')) > 3:
            #on_click = get_stud_info(stud_id, subject_name)
            chek = st.sidebar.checkbox('Выделить только нули',value=False)
            if chek:
                get_stud_info(stud_id, subject_name,only_nulls = True)
            else:
                get_stud_info(stud_id, subject_name)
            #st.sidebar.button('Поехали', on_click=get_stud_info(stud_id, subject_name))
    except KeyError:
        st.text('...что-то у нас не получается найти преподавателя с таким именем...')


#stud_id = st.text_input('Введите id', key='input')

#st.button('Запустить вычисление', on_click=get_stud_info(stud_id, subject_name))



