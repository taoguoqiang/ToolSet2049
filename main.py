import jielong
import streamlit as st

text_input = st.text_area(label='请输入接龙信息:', height=200)
if st.button("点击排序", type="primary", use_container_width=True):
    jielong.save_text_to_file(text_input)
    st.title('排序结果:')
    st.text(jielong.sort_sales())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    i = 0

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
