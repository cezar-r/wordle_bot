def read_file(filename):
	file = open(filename)
	content = []
	for word in file.readlines():
		content.append(word.strip())
	return set(content)


WORDBANK = read_file("wordbank.txt")
PREV_ANSWERS = read_file("prev_answers.txt")