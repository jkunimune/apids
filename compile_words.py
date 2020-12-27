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
		category = "obscure"
	elif "70" in filename:
		category = "obscure"
	elif "80" in filename:
		category = "obscure"
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
						words.append((len(word), word, category)) # save it a a word
					if num_letters == 7 and category not in ["apiary", "obscure", "fake", "variant"] and not ("'" in word and "s" in word.lower()) \
							and not word.endswith('s') and not word.endswith('ed') and not word.endswith('ing'):
						pangrams.append(word.lower()) # and as a pangram, if applicable
	except FileNotFoundError:
		pass

for i, (length, word, category) in enumerate(words): # apply score bonuses
	if category == 'fake':
		score_bonus = 3
	elif category in ['obscure', 'memetic']:
		score_bonus = 2
	elif category in ['apiary', 'hacker', 'variant', 'Abbr.']:
		score_bonus = 1
	else:
		score_bonus = 0
	words[i] = (length + score_bonus, word, category)
words.sort()

with open("wordlists/words", 'w') as f:
	for value, word, category in words:
		f.write("{:d}\t{:s}\t{:s}\n".format(value, word, category))

with open("wordlists/pangrams", 'w') as f:
	f.write("{:d}\n".format(len(pangrams)))
	for word in pangrams:
		f.write("{:s}\n".format(word))
