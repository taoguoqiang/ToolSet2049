import pandas as pd


def save_text_to_file(text_str):
    with open('接龙.txt', 'w', encoding='utf-8') as file:
        file.write(text_str)


def get_sales_count(line, para_start, para_end):
    para_start = para_start.replace(' ', '')
    para_end = para_end.replace(' ', '')

    start_index = line.find(para_start) + len(para_start)

    max_para_len = 5
    end_index = line[start_index:].find(para_end) + start_index

    if end_index <= start_index:
        sale_num = 0
    else:
        if end_index - start_index > max_para_len:
            end_index = start_index + max_para_len
        sale_num = int(line[start_index:end_index])

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
    print(result)

    return result
