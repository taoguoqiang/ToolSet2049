import pandas as pd
import re

record_xlsx_column_parent_str = '家长'
record_xlsx_column_kid_str = '小孩'
record_xlsx_column_age_str = '年龄'
record_xlsx_column_retail_sale_str = '零售'
record_xlsx_column_batch_sale_str = '批发'
record_xlsx_column_total_sale_str = '总量'
record_xlsx_column_update_date_str = '更新日期'
record_xlsx_columns = [record_xlsx_column_parent_str,
                       record_xlsx_column_kid_str,
                       record_xlsx_column_age_str,
                       record_xlsx_column_retail_sale_str,
                       record_xlsx_column_batch_sale_str,
                       record_xlsx_column_total_sale_str,
                       record_xlsx_column_update_date_str]


def get_date_from_strlines(filepath='接龙.txt'):
    with open(filepath, "r", encoding='utf-8') as f:
        # 逐行读取文件内容
        lines = f.readlines()
    for line in lines:
        print(line)
        pattern = r"\d+月\d+日"
        match = re.search(pattern, line)
        if match:
            return match.group(0)


def remove_non_digits(s):
    # print(s)
    return re.sub(r'[^\d]', '', s)


def save_text_to_file(text_str):
    with open('接龙.txt', 'w', encoding='utf-8') as file:
        file.write(text_str)


def get_sales_count(line, para_start, para_end):
    para_start = para_start.replace(' ', '')
    para_end = para_end.replace(' ', '')
    line = line.replace(' ', '')

    # print(para_start, para_end)
    start_index = line.find(para_start)
    # print(start_index)
    if start_index <= 0:
        return 0

    start_index += len(para_start)
    end_index = 0
    max_para_len = 5

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

        match = re.search(r'\d+', line[start_index:end_index])
        try:
            sale_num = int(match.group(0))
        except:
            print('exception:', line[start_index:end_index])
            sale_num = 0

    return sale_num


def seperate_personal(filepath='接龙.txt'):
    # 打开txt文件，文件路径为file_path
    with open(filepath, "r", encoding='utf-8') as f:
        # 逐行读取文件内容
        jielong_str_lines = f.readlines()

    lines_per_person = ''
    records_in_persons = []

    # seperate by person
    for line in jielong_str_lines:
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
    # print(df_sorted)

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
    if '石家庄' in line:
        i = line[start_index:].find('石家庄') + len('石家庄')
        end_index = line[i:].find(para_end) + i
    else:
        end_index = line[start_index:].find(para_end)

    name_of_parent = ''
    if end_index <= 0:
        return ''

    end_index += start_index
    start_index = find_first_chinese_char(line[start_index:end_index])

    if start_index < 0:
        return ''

    try:
        name_of_parent = line[start_index:end_index]
        # print(start_index, end_index, name_of_parent)
    except:
        print('exception:', line[start_index:end_index])
        name_of_parent = line[0:end_index]
        # print(name_of_parent)

    return name_of_parent


def record_str_to_data_list(personal_record):
    parent_name = get_name_of_parent(personal_record)
    total_sale = get_sales_count(personal_record, '累计', '本')
    batch_sale = get_sales_count(personal_record, '批发', '本')
    retail_sale = total_sale - batch_sale

    return [parent_name, retail_sale, batch_sale, total_sale]


def update_sales_to_record_xlsx(record_xlsx_data):
    records_in_persons = seperate_personal()
    # print(records_in_persons)
    if len(records_in_persons) <= 0:
        print('No data!')
        return

    update_date = get_date_from_strlines()

    if len(record_xlsx_data) <= 0:
        record_xlsx_data = pd.DataFrame(columns=record_xlsx_columns)

    # get sales number for each person
    for record in records_in_persons:
        sale_num_info = record_str_to_data_list(record)
        parent_str = sale_num_info[0]
        retail_int = sale_num_info[1]
        batch_int = sale_num_info[2]
        total_int = sale_num_info[3]

        if len(parent_str) <= 0:
            continue
        print(parent_str, retail_int, batch_int, total_int)
        # 查找首列内容等于A的行
        row_index = record_xlsx_data[record_xlsx_data[record_xlsx_column_parent_str] == parent_str].index

        # 如果找到了这样的行，更新第三列和第四列的数据
        if not row_index.empty:
            record_xlsx_data.at[row_index[0], record_xlsx_column_retail_sale_str] = retail_int
            record_xlsx_data.at[row_index[0], record_xlsx_column_batch_sale_str] = batch_int
            record_xlsx_data.at[row_index[0], record_xlsx_column_total_sale_str] = total_int
            record_xlsx_data.at[row_index[0], record_xlsx_column_update_date_str] = update_date
        else:
            print(parent_str)
            # 如果未找到，新增一行
            new_row = [parent_str,
                       '',
                       '',
                       retail_int,
                       batch_int,
                       total_int,
                       update_date
                       ]
            record_xlsx_data.loc[len(record_xlsx_data)] = new_row

    filename = update_date + '.xlsx'
    record_xlsx_data.to_excel(filename, index=False)

    return record_xlsx_data

