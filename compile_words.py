filenames = []
for size in [10, 20, 35, 40, 50]:
	for category in ["words", "contractions", "abbreviations", "upper"]:
		filenames.append("english-{:s}.{:d}".format(category, size))
		filenames.append("american-{:s}.{:d}".format(category, size))
filenames.append("special-hacker.50")
filenames.append("yumbology")

seen = set()
words = []
pangrams = []

for filename in filenames:
	if "hacker" in filename:
		category = "hacker"
	elif "abbrev" in filename:
		category = "abbr."
	elif "variant" in filename:
		category = "variant"
	elif "10" in filename:
		category = "basic"
	elif "50" in filename:
		category = "apiary"
	else:
		category = "normal"
	try:
		with open("wordlists/{}".format(filename), 'r') as f:
			word = f.readline()
			while len(word) > 0:
				word = f.readline()
				if len(word) == 0:
					break
				word = word.strip()
				if len(word) >= 4:
					if word == "nigger" or word == "nigger's" or word == "niggers":
						continue
					if word.lower() in seen:
						continue
					seen.add(word.lower())
					num_letters = len(set(word.lower()))
					if num_letters <= 7:
						words.append([len(word), word, category])
					if num_letters == 7:
						pangrams.append(word.lower())
	except FileNotFoundError:
		pass

with open("wordlists/words", 'w') as f:
	for length, word, category in words:
		f.write("{:d}\t{:s}\t{:s}\n".format(length, word, category))

with open("wordlists/pangrams", 'w') as f:
	for word in pangrams:
		f.write("{:s}\n".format(word))
