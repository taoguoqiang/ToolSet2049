import pandas as pd


def save_text_to_file(text_str):
    with open('接龙.txt', 'w', encoding='utf-8') as file:
        file.write(text_str)


def get_sales_count(line):
    start_index = line.find("成交") + 2
    end_index = line.find("本")
    sale_num = int(line[start_index:end_index])
    # print(sale_num)
    return sale_num


def sort_sales(filepath='接龙.txt'):
    # 打开txt文件，文件路径为file_path
    with open(filepath, "r", encoding='utf-8') as f:
        # 逐行读取文件内容
        lines = f.readlines()

    records_in_persons = []
    lines_per_person = ''

    sales_counts = []

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

    # get sales number for each person
    for record in records_in_persons:
        if "成交" in record:
            sales_counts.append((get_sales_count(record)))
            # print("-----------")
            # print(record)
        else:
            sales_counts.append(0)
            # print(record)

    df = pd.DataFrame({'成交数': sales_counts, 'text': records_in_persons})
    df_sorted = df.sort_values('成交数', ascending=False)
    # print(df_sorted)

    print_out = ''
    index = 1
    for i in df_sorted['text']:
        i = i[i.find("."):]
        if len(i) == 0:
            continue
        i = str(index) + i
        print_out += i
        index += 1

    # print(print_out)

    return print_out
