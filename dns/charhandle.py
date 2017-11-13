def get_request(your_list):
    my_list = []
    new_list = []
    my_list.extend(your_list)
    re_list = []
    thelen = my_list[0]
    try:
        while thelen != 0:
            for ml in my_list[1:thelen + 1]:
                new_list.append(chr(ml))
            my_list[0:thelen + 1] = []
            thelen = my_list[0]
            new_list.append('.')
    except IndexError:
        print("bao wen ge shi bu dui")
    new_list.pop()
    return new_list

