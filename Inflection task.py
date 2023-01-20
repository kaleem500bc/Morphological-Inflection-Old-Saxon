import collections


def input_to_listoflist(input_file):
    file_lines = [line.rstrip('\n') for line in input_file]
    temp_list = []
    for i in file_lines:
        temp_list.append(i.split())
    return temp_list


# # returns longest common substring
# def get_stem(string1, string2):
#     answer = ""
#     len1, len2 = len(string1), len(string2)
#     for i in range(len1):
#         match = ""
#         for j in range(len2):
#             if (i + j < len1 and string1[i + j] == string2[j]):
#                 match += string2[j]
#             else:
#                 if (len(match) > len(answer)): answer = match
#                 match = ""
#     return answer


# returns longest common substring
def get_stem(str1, str2):
    lcs = ""
    longest_temp = ""
    for i in range(0, len(str1)):
        for j in range(0, len(str2)):
            if str1[i] == str2[j]:
                # longest_temp += str1[i]
                (i_temp, j_temp) = (i, j)
                while i_temp < len(str1) and j_temp < len(str2) and str1[i_temp] == str2[j_temp]:
                    longest_temp += str1[i_temp]
                    i_temp += 1
                    j_temp += 1
            lcs = longest_temp if len(longest_temp) > len(lcs) else lcs
            longest_temp = ""
    return lcs


# calculates the levenshtein distance
def lev_dist(lemma, inflected):
    # stem = get_stem(lemma, inflected)
    # pre_cnt = lemma.find(stem)

    # the following block of code replaced the above to make it case insensitive
    # for the entry LoC	loCced	V;PST
    stem = get_stem(lemma.lower(), inflected.lower())
    temp = lemma.lower()
    pre_cnt = temp.find(stem)

    inf_pre_cnt = inflected.lower().find(stem)
    suf_index = len(stem)
    return [pre_cnt, suf_index, inf_pre_cnt]


def get_transformation_dicts(list_arg):
    suf_dict = collections.defaultdict(dict)
    pre_dict = collections.defaultdict(dict)

    for entry in list_arg:
        (lemma, inflected, inflection) = tuple(entry)
        (pre_cnt, suf_index, inf_pre_cnt) = tuple(lev_dist(lemma, inflected))
        # populate the suffix dictionary
        i = suf_index
        while i >= pre_cnt:
            suf_dict[lemma[i:len(lemma)]][inflection] = inflected[i:len(inflected)]
            i -= 1
        # populate the prefix dictionary
        pre_dict[lemma[0:pre_cnt]][inflection] = inflected[0:inf_pre_cnt]
    return[suf_dict, pre_dict]


def conversion(list_arg, suffix_dict, prefix_dict):
    conversion_dict = collections.defaultdict(dict)
    for entry in list_arg:
        lemma = entry[0]
        inflected = entry[0]
        inflection = entry[2]

        # get the new suffix
        for i in range(0, len(lemma)):
            if lemma[i:len(lemma)] in suffix_dict:
                if inflection in suffix_dict[lemma[i:len(lemma)]]:
                    new_suffix = suffix_dict[lemma[i:len(lemma)]][inflection]
                    # replaces lemma suffix with inflected suffix
                    inflected = lemma[0:i] + new_suffix
                continue

        # get the new prefix
        for i in reversed(range(0, len(lemma))):
            if lemma[0:i] in prefix_dict:
                if inflection in prefix_dict[lemma[0:i]]:
                    new_prefix = prefix_dict[lemma[0:i]][inflection]
                    # replaces lemma prefix with inflected prefix
                    inflected = new_prefix + inflected[i:len(inflected)]
                continue

        conversion_dict[lemma][inflection] = inflected
    return conversion_dict

# edit this line with respect to the path of the files
train = input_to_listoflist(open('old-saxon-train-medium', encoding="utf8"))
dev = input_to_listoflist(open('old-saxon-dev', encoding="utf8"))

suffix_dict, prefix_dict = tuple(get_transformation_dicts(train))



y = conversion(dev, suffix_dict, prefix_dict)

print(prefix_dict)
print("\n\n\n\n\n\n")
print(suffix_dict)

checker_list = []
for i in y:
    # print(i)
    for k in y[i]:

        print(i, k, y[i][k])
        checker_list.append([i, y[i][k], k])

count = 0
for i in dev:
    i0 = i[0]
    i2 = i[2]

    if y[i[0]][i[2]] == i[1]:
        count += 1
        # print(y[i[0]][i[2]], i[1])
    # else:
    #     print(y[i[0]][i[2]], i[1])
print("\n\n", (count/len(dev))*100)



