import pandas as pd
import re

record_xlsx_path = '累计数据.xlsx'
record_xlsx_column_parent_str = '家长'
record_xlsx_column_kid_str = '小孩'
record_xlsx_column_age_str = '年龄'
record_xlsx_column_retail_sale_str = '零售'
record_xlsx_column_batch_sale_str = '批发'
record_xlsx_column_total_sale_str = '总量'
jielong_str_lines = ''


def remove_non_digits(s):
    # print(s)
    return re.sub(r'[^\d]', '', s)


def save_text_to_file(text_str):
    with open('接龙.txt', 'w', encoding='utf-8') as file:
        file.write(text_str)


def get_sales_count(line, para_start, para_end):
    para_start = para_start.replace(' ', '')
    para_end = para_end.replace(' ', '')

    # print(para_start, para_end)
    start_index = line.find(para_start) + len(para_start)
    end_index = 0
    max_para_len = 8

    end_index = line[start_index:].find(para_end) + start_index

    if end_index <= start_index:
        # sale_num = 0
        return 0
    else:
        if end_index - start_index > max_para_len:
            start_index = line[end_index:].find(para_start) + len(para_start)
            start_index = start_index + end_index
            end_index = line[start_index:].find(para_end) + start_index

            if end_index <= start_index:
                # sale_num = 0
                return 0

        # print(line, line[start_index:end_index])
        try:
            sale_num = int(remove_non_digits(line[start_index:end_index]))
        except:
            print('exception:', line[start_index:end_index])
            sale_num = int(remove_non_digits(line[start_index:end_index]))
            # print(sale_num)

    # print(sale_num)
    return sale_num


def seperate_personal(filepath='接龙.txt'):
    # 打开txt文件，文件路径为file_path
    with open(filepath, "r", encoding='utf-8') as f:
        # 逐行读取文件内容
        lines = f.readlines()

    lines_per_person = ''
    records_in_persons = []

    # seperate by person
    for line in lines:
        # format the wrong inputs
        if " ·" in line:
            line = line.replace("·", ".")

        if ". " not in line:
            lines_per_person += line
        else:
            # print(lines_per_person)
            records_in_persons.append(lines_per_person)
            # print(records_in_persons)
            # print("-----------")

            lines_per_person = ''
            lines_per_person += line

    if len(lines_per_person) > 0:
        records_in_persons.append(lines_per_person)

    return records_in_persons


def sort_sales(para_start='累计收入', para_end='元'):
    records_in_persons = seperate_personal()

    sales_counts = []
    # get sales number for each person
    for record in records_in_persons:
        if para_start in record:
            sales_counts.append((get_sales_count(record, para_start, para_end)))
            # print("-----------")
            # print(record)
        else:
            sales_counts.append(0)
            # print(record)

    df = pd.DataFrame({'成交数': sales_counts, 'text': records_in_persons})
    df_sorted = df.sort_values('成交数', ascending=False)
    print(df_sorted)

    print_out = ''
    seq_title = ["\n第一名", "\n第二名", "\n第三名", "\n第四名", "\n第五名",
                 "\n第六名", "\n第七名", "\n第八名", "\n第九名", "\n第十名",
                 "\n第十一名", "\n第十二名", "\n第十三名", "\n第十四名", "\n第十五名",
                 "\n第十六名", "\n第十七名", "\n第十八名", "\n第十九名", "\n第二十名",
                 "\n第二十一名", "\n第二十二名", "\n第二十三名", "\n第二十四名", "\n第二十五名",
                 "\n第二十六名", "\n第二十七名", "\n第二十八名", "\n第二十九名", "\n第三十名",
                 "\n第三十一名", "\n第三十二名", "\n第三十三名", "\n第三十四名", "\n第三十五名",
                 "\n第三十六名", "\n第三十七名", "\n第三十八名", "\n第三十九名", "\n第四十名",
                 "\n第四十一名", "\n第四十二名", "\n第四十三名", "\n第四十四名", "\n第四十五名",
                 "\n第四十六名", "\n第四十七名", "\n第四十八名", "\n第四十九名", "\n第五十名",
                 ]
    last_top_sales = -1
    top_sales = 0
    seq = 0
    for index, row in df_sorted.iterrows():
        top_sales = row['成交数']
        i = row['text']

        i = i[i.find("."):]
        if len(i) == 0:
            continue
        if top_sales == last_top_sales:
            print_out += i
        else:
            if seq < len(seq_title):
                print_out += seq_title[seq] + i
                seq += 1
            else:
                break

        last_top_sales = top_sales

    result = print_out.replace('.', '')
    # print(result)

    return result


def find_first_chinese_char(s):
    # 定义一个正则表达式，匹配任何中文字符
    pattern = re.compile(r'[\u4e00-\u9fff]')

    # 在字符串中搜索第一个匹配的非中文字符
    match = pattern.search(s)

    # 如果找到了匹配，返回它的位置
    if match:
        return match.start()
    else:
        # 如果没有找到非中文字符，返回-1或者None
        return -1


def get_name_of_parent(line, para_start='.', para_end='家'):
    para_start = para_start.replace(' ', '')
    para_end = para_end.replace(' ', '')

    start_index = 0
    end_index = line[start_index:].find(para_end) + start_index

    name_of_parent = ''
    if end_index <= 0:
        return ''

    start_index = find_first_chinese_char(line[start_index:end_index])

    if start_index < 0:
        return ''

    try:
        name_of_parent = line[start_index:end_index]
    except:
        print('exception:', line[start_index:end_index])
        name_of_parent = line[0:end_index]
        print(name_of_parent)

    return name_of_parent


def record_str_to_data_list(personal_record):
    parent_name = get_name_of_parent(personal_record)
    total_sale = get_sales_count(personal_record, '累计', '本')
    batch_sale = get_sales_count(personal_record, '批发', '本')
    retail_sale = total_sale - batch_sale

    return [parent_name, retail_sale, batch_sale, total_sale]


def update_sales_to_record_xlsx():
    records_in_persons = seperate_personal()
    record_xlsx_data = pd.read_excel(record_xlsx_path)

    # get sales number for each person
    for record in records_in_persons:
        sale_num_info = record_str_to_data_list(record)
        parent_str = sale_num_info[0]
        retail_int = sale_num_info[1]
        batch_int = sale_num_info[2]
        total_int = sale_num_info[3]

        if len(parent_str) <= 0:
            continue

        # 查找首列内容等于A的行
        row_index = record_xlsx_data[record_xlsx_data[record_xlsx_column_parent_str] == parent_str].index

        # 如果找到了这样的行，更新第三列和第四列的数据
        if not row_index.empty:
            record_xlsx_data.at[row_index[0], record_xlsx_column_retail_sale_str] = retail_int
            record_xlsx_data.at[row_index[0], record_xlsx_column_batch_sale_str] = batch_int
            record_xlsx_data.at[row_index[0], record_xlsx_column_total_sale_str] = total_int
        else:
            # 如果未找到，新增一行
            new_row = [parent_str,
                       '',
                       '',
                       retail_int,
                       batch_int,
                       total_int
                       ]
            record_xlsx_data.loc[len(record_xlsx_data)] = new_row

    record_xlsx_data.to_excel('累计数据.xlsx')
