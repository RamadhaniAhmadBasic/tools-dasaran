def f(title, content):
	formatted_title = "|" + title.center(42) + "|"

	chunk_size = 40  # Adjust this value as needed
	words = content.split()
	lines = []
	current_line = ""

	for word in words:
		if len(current_line) + len(word) <= chunk_size:
			current_line += word + " "
		else:
			lines.append(current_line)
			current_line = word + " "
	if current_line:
		lines.append(current_line)

	print("+==========================================+")
	print(formatted_title)
	print("+==========================================+")
	for line in lines:
		formatted_line = "|" + line.strip().center(42) + "|"
		print(formatted_line)
	print("+==========================================+")
	input("Press enter to continue ...")