def merge_text_file(first_filename, second_filename, merged_filename):
    '''
    Merge two text files, the sequence of two file's content maybe changed.
    example:
    source_file_1 = "a.txt"
    source_file_2 = "b.txt"
    merged_file = "merged.txt"
    merge_text_file(source_file_1, source_file_2, merged_file)
    '''
    first_list = open(first_filename, 'r').read().split('\n')
    second_list = open(second_filename, 'r').read().split('\n')

    result_set = set(first_list) | set(second_list)
    result_list = list(result_set)
    result_list.sort()
    result_file = open(merged_filename, "w")
    for item in result_list:
        temp = item.strip()
        if temp == "": continue
        result_file.write(temp + '\n')

    result_file.close()
