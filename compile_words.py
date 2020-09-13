filenames = [] # compile a list of filenames from least to most interesting words
for size in [10, 20, 35, 40, 50, 55, 60, 70]:
	for category in ["words", "contractions", "abbreviations"]:
		filenames.append("english-{:s}.{:d}".format(category, size))
		filenames.append("american-{:s}.{:d}".format(category, size))
		filenames.append("variant_1-{:s}.{:d}".format(category, size))
		filenames.append("variant_2-{:s}.{:d}".format(category, size))
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
	elif "55" in filename:
		category = "apiary"
	elif "60" in filename:
		category = "ultra"
	elif "70" in filename:
		category = "ultra"
	elif "80" in filename:
		category = "ultra"
	elif "95" in filename:
		category = "fake"
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
					if word == "nigger" or word == "nigger's" or word == "niggers": # with the exception of a short ban list
						continue
					if word.lower() in seen: # and making sure to avoid taking words multiple times (this is rarely an issue)
						continue
					seen.add(word.lower())
					num_letters = len(set(word.lower())) # count the letters
					if num_letters <= 7:
						words.append([word, len(word), category]) # save it a a word
					if num_letters == 7 and category not in ["apiary", "ultra", "fake", "variant"]:
						pangrams.append(word.lower()) # and as a pangram, if applicable
	except FileNotFoundError:
		pass

with open("wordlists/words", 'w') as f:
	for word, length, category in words:
		if category == 'fake':
			score_bonus = 3
		elif category == 'ultra':
			score_bonus = 2
		elif category in ['apiary', 'memetic', 'hacker', 'variant', 'Abbr.']:
			score_bonus = 1
		else:
			score_bonus = 0
		f.write("{:s}\t{:d}\t{:s}\n".format(word, length + score_bonus, category))

with open("wordlists/pangrams", 'w') as f:
	f.write("{:d}\n".format(len(pangrams)))
	for word in pangrams:
		f.write("{:s}\n".format(word))
