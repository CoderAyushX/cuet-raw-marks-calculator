from PyPDF2 import PdfReader
import re

def calculate_marks(res_pdf,q_from, q_to, a_from, a_to):
    # File reader class
    reader = PdfReader(res_pdf)
    ans_reader = PdfReader("answer_key.pdf")
    # ans key
    ans_page_range = range(a_from-1, a_to-1)
    # res sheet
    page_range = range(q_from-1, q_to)

    # To remove same answers and id
    def remove_duplicate_pairs(lst):
        unique_values = {}
        result = []

        for pair in lst:
            key = tuple(pair)

            if key in unique_values:
                continue
            else:
                unique_values[key] = pair
                result.append(pair)

        return result

    # Regex patterns
    question_pattern = r'Question ID : (\d+)'
    answer_pattern = r"Option \d+ ID : (\d+.*?\d+)"
    chosen_pattern = r'Chosen Option : ([1-4]|--)'
    answer_key_pattern = r'\b(\d{10,}|DROP)(?=\b|\D)'

    # Final lists
    question_ids = []
    answer_ids = []
    chosen_ids = []
    answer_matches = []

    # Getting all text from the answer pdf
    for i in ans_page_range:
        ans_page = ans_reader.pages[i]
        page_text = ans_page.extract_text()

        temp_answer_matches = re.findall(answer_key_pattern, page_text)
        answer_matches.extend(temp_answer_matches)

    # Turning str into int in the answer
    answer_key_ids = []
    for i in answer_matches:
        if i == "DROP":
            answer_key_ids.append(0000000000)
        else:
            answer_key_ids.append(int(i))

    # Page range
    for i in page_range:
        page = reader.pages[i]

        # Extracting the page text
        page_text = page.extract_text()

        # Getting the ids
        temp_question_ids = re.findall(question_pattern, page_text)
        question_ids.extend(temp_question_ids)

        # Getting the options number and ids
        output = re.findall(answer_pattern, page_text)
        modified_matches = [match.replace(' ', '') if ' ' in match else match for match in output]
        answer_ids.extend(modified_matches)

        # Getting chosen option
        temp_chosen_ids = re.findall(chosen_pattern, page_text)
        chosen_ids.extend(temp_chosen_ids)

    answer_ids = [answer_ids[i:i+4] for i in range(0, len(answer_ids), 4)]

    print(len(question_ids), " ", len(answer_ids), " ", len(chosen_ids))

    # This code will make a list which gives a list of question id and selected option
    question_n_answer_id = []
    for index, sublist in enumerate(answer_ids):
        # Getting question id and value and making a list
        sublist_ids, sublist_values = zip(*[(str(index+1), int(pair)) for index, pair in enumerate(sublist)])
        sublist_ids = list(sublist_ids)
        sublist_values = list(sublist_values)

        # Getting question id
        question_id = int(question_ids[index])

        if chosen_ids[index] in sublist_ids:
            chosen_idx = sublist_ids.index(chosen_ids[index])
            chosen_value = sublist_values[chosen_idx]
            question_n_answer_id.extend([[question_id, chosen_value]])
        else:
            question_n_answer_id.extend([[question_id, False]])

    # Getting answer id and key list
    answer_key = []
    for i in range(0, len(answer_key_ids), 2):
        answer_key.append(answer_key_ids[i:i+2])



    # all unique answer keys
    final_answer_key = remove_duplicate_pairs(answer_key)

    print(len(final_answer_key))
    marks = 0
    for index, pair in enumerate(question_n_answer_id):
        real_index = index+1
        if pair[1] == False:
            marks += 0
            print(real_index, "0 marks:" , pair)
        elif pair in final_answer_key:
            marks +=5
            print(real_index, "5 marks:" , pair)
        elif pair not in final_answer_key:
            marks -= 1
            print(real_index, "-1 marks:" , pair)

    return(marks)





