import pandas as pd
import jielong
import streamlit as st


def try_read_csv(filename):
    # 尝试使用常见编码类型
    encodings = ['utf-8', 'gbk', 'gb2312']
    for encoding in encodings:
        try:
            df = pd.read_csv(filename, encoding=encoding)
            print(f"文件读取成功，使用的编码为: {encoding}")
            return df
        except UnicodeDecodeError:
            print(f"尝试编码: {encoding} 失败")


st.title('接龙数据排序')
text_input = st.text_area(label='请输入接龙信息:', height=200)


tab1, tab2, tab3 = st.tabs(["当日排序", "累计排序", "保存数据"])
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

with tab3:
    uploaded_data = pd.DataFrame()
    uploaded_file = st.file_uploader("上传文件xlsx or csv")
    if uploaded_file is not None:
        st.write("filename:", uploaded_file.name)
        if 'xlsx' in uploaded_file.name:
            uploaded_data = pd.read_excel(uploaded_file)
        elif 'csv' in uploaded_file.name:
            uploaded_data = try_read_csv(uploaded_file)

    if st.button("更新表格", type="primary", use_container_width=True) and len(text_input) > 0:
        jielong.save_text_to_file(text_input)
        updated_data = jielong.update_sales_to_record_xlsx(uploaded_data)
        st.dataframe(updated_data, use_container_width=True, hide_index=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    i = 0
    # jielong.sort_sales()
    # uploaded_data = pd.DataFrame()
    # uploaded_data = pd.read_excel('6月9日.xlsx')
    # uploaded_data = pd.read_csv('6月8日.CSV', encoding='gbk')
    # jielong.update_sales_to_record_xlsx(uploaded_data)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
