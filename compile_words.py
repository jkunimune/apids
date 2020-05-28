filenames = [] # compile a list of filenames from least to most interesting words
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
	if "hacker" in filename: # each one has an associated category name
		category = "hacker"
	elif "abbrev" in filename:
		category = "Abbr."
	elif "yumbo" in filename:
		category = "memetic"
	elif "variant" in filename:
		category = "variant"
	elif "10" in filename:
		category = "basic"
	elif "50" in filename:
		category = "apiary"
	else:
		category = "normal"
	try:
		with open("wordlists/{}".format(filename), 'r') as f: # open them all
			while True:
				line = f.readline()
				if len(line) == 0: # read until we are out of lines
					break
				word = line.strip() # pull out the word
				if len(word) >= 4:
					if word == "nigger" or word == "nigger's" or word == "niggers": # with the exception of a short blacklist
						continue
					if word.lower() in seen: # and making sure to avoid taking words multiple times (this is rarely an issue)
						continue
					seen.add(word.lower())
					num_letters = len(set(word.lower())) # count the letters
					if num_letters <= 7:
						words.append([word, len(word), category]) # save it a a word
					if num_letters == 7 and category != "apiary":
						pangrams.append(word.lower()) # and as a pangram, if applicable
	except FileNotFoundError:
		pass

with open("wordlists/words", 'w') as f:
	for word, length, category in words:
		f.write("{:s}\t{:d}\t{:s}\n".format(word, length+(1 if category in ['apiary', 'memetic', 'hacker'] else 0), category))

with open("wordlists/pangrams", 'w') as f:
	f.write("{:d}\n".format(len(pangrams)))
	for word in pangrams:
		f.write("{:s}\n".format(word))
