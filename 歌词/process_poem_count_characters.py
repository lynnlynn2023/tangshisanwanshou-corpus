import re
# Define
input_txt = '野孩子.txt'
output_txt = 'result' + input_txt

# Function to split Chinese text into sentences
def split_chinese_text(text):
    sentences = re.split(r'[ 。！？，,.]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

# Read input text file
with open(input_txt, 'r', encoding='utf-8') as input_file:
    input_lines = input_file.readlines()



# Write output to a new text file
with open(output_txt, 'w', encoding='utf-8') as output_file:
    for line in input_lines:
        # Split the text into sentences
        sentences = split_chinese_text(line)
        for sentence in sentences:
            char_count = len(sentence)
            output_file.write(f'【{char_count}】{sentence}')
        output_file.write('\n')

print(f"Output file {output_txt} has been created.")
