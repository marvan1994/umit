import streamlit_survey as ss
import streamlit as st
from load_css import local_css


st.set_page_config(page_title='Исследование занятости',
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
survey = ss.StreamlitSurvey('Исследование занятости')
pages = survey.pages(2, on_submit=lambda: st.success("Ваши ответы были записаны. Спасибо за участие!"))
with pages:
    if pages.current == 0:
        st.write("Вы учитесь в школе?")
        used_before = survey.radio(
            "school_learn",
            options=["->", "Да", "Нет"],
            index=0,
            label_visibility="collapsed",
            horizontal=True,
        )
        if used_before == "Да":
            st.write("Как много времени вы проводите в школе?")
            survey.select_slider(
                "st_frequency",
                options=["Один - Два часа", "Три - четыре часа", "Пять - шесть часов", "Шесть - семь часов", "Более семи часов"],
                label_visibility="collapsed",
            )
        elif used_before == "Нет":
            st.write("Если вы не ходите в школу, то как вы получаете среднее образование?")
            used_other = survey.radio(
                "no_school",
                options=["->", "На домашнем обучении", "В онлайн формате"],
                index=0,
                label_visibility="collapsed",
                horizontal=True,
            )
            if used_other == "В онлайн формате":
                st.write("В какой онлайн школе?")
                survey.multiselect(
                    "other_tools",
                    options=["Умскул", "В плохой онлайн школе"],
                    label_visibility="collapsed",
                )
    elif pages.current == 1:
        st.write("Как вам наше исследование?")
        survey.select_slider(
            "Общая удовлетворенность",
            options=["Совсем не понравилось", "Так себе опрос", "Ничего примечательного", "В целом окей", "Очень понравилось"],
            label_visibility="collapsed",
        )
