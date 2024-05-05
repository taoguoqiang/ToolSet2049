import jielong
import streamlit as st

st.title('接龙数据排序')
text_input = st.text_area(label='请输入接龙信息:', height=200)


tab1, tab2 = st.tabs(["当日排序", "累计排序"])
with tab1:
    para_start1 = st.text_input("输入排序关键词", "成交")
    para_end1 = st.text_input("输入结束关键词", "本")
    if st.button("当日排序", type="primary", use_container_width=True) and len(text_input) > 0:
        jielong.save_text_to_file(text_input)
        st.title('排序结果:')
        # print(para_start1, para_end1)
        st.text(jielong.sort_sales(para_start1, para_end1))

with tab2:
    para_start2 = st.text_input("输入排序关键词", "累计收入")
    para_end2 = st.text_input("输入结束关键词", "元")
    if st.button("累计排序", type="primary", use_container_width=True) and len(text_input) > 0:
        jielong.save_text_to_file(text_input)
        st.title('排序结果:')
        # print(para_start2, para_end2)
        st.text(jielong.sort_sales(para_start2, para_end2))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    i = 0
    jielong.sort_sales()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
