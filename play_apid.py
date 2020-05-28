import sys, codecs

if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
	utf8_writer = codecs.getwriter('UTF-8')
	if sys.version_info.major < 3:
		sys.stdout = utf8_writer(sys.stdout, errors='replace')
	else:
		sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')

import bisect
import random

while True:
	with open('wordlists/pangrams', 'r') as f:
		pangram_index = random.randint(0, int(f.readline()))
		for i in range(pangram_index):
			f.readline()
		pangram = f.readline().strip()

	letters = set(pangram.lower())
	bolded = random.choice(list(letters))

	gotten = [] # list of [word, score value, category, number of hints taken]
	remaining = [] # list of [word, score value, category, number of hints taken]
	max_score = 0 # max possible score
	with open('wordlists/words', 'r') as f:
		while True:
			line = f.readline()
			if len(line) == 0:
				break
			word, value, category = line.strip().split('\t')
			if bolded in word.lower() and set(word.lower()).issubset(letters):
				remaining.append([word, int(value), category, 0])
				max_score += int(value)

	if len(remaining) < 20 or len(remaining) >= 60: # make sure the number of words is reasonable
		continue
	break

def print_letters():
	print()
	hexen = [c.upper() for c in letters]
	hexen.remove(bolded.upper())
	random.shuffle(hexen) # randomize the order of the
	print("   {1}   {2}   \n\n {3}  [{0}]  {4} \n\n   {5}   {6}   ".format(bolded.upper(), *hexen)) # hexagons!
	print()

def print_gotten():
	print()
	if len(gotten) == 0:
		print("You have gotten 0 words.")
		print()
		return

	for i, (word, value, category, hints) in enumerate(gotten): # print all the gotten words
		print("{2[0]:s}{1:1d}:{0:9s}".format(word, value, category), end=['  ', '  ', '\n'][i%4]) # in four columns
	if i%4 != 3:
		print()
	print()
	
def print_histogram():
	print()
	for length in range(4, 20):
		count = {}
		for word, value, category, hints in remaining:
			if len(word) == length:
				count[category] = count.get(category, 0) + 1
		if sum(count.values()) >= 4: # if there are a lot of words of this length
			print("{:2d} {:d}-letter words".format(sum(count.values()), length)) # just print that entire total
		else: # if there are only a few
			for category in sorted(count.keys()): # break it up by category
				print("{:2d} {:d}-letter {:s} word{:s}".format(count[category], length, category, "s" if count[category] > 1 else ""))
	print()

def print_hint():
	print()
	remain = remaining[0]
	if remain[3] == 0:
		remain[3] += 1 # the first hint costs double
		remain[1] -= 1
	word, value, category, hints = remain
	if len(word) - hints < 0:
		print("Seriously? I literally gave you the entire word. {}.".format(word))
	else:
		hint = "•"*(len(word) - hints) + word[-hints:] # give the last few letters
		print("Remaining {:s} word: {}".format(remain[2], hint))
	remain[3] += 1 # remember this hint
	remain[1] -= 1 # decrement the value
	print()

def get_word(get):
	for i, (word, value, category, hints) in enumerate(remaining):
		if get == word:
			bisect.insort(gotten, remaining.pop(i))
			print(random.choice(["Yep!","Jes!","Ye got it!","Yeah!","Yea!","Yee!","Ya!","Yas!","Yeet!","un!","si!"]), end='')
			if word == pangram:
				print(" And that was the pangram!")
			else:
				print()
			return value
	print(random.choice(["Nope.","Ne.","Alas.","Not.","Nah.","Nay.",u"Нет.","no."]))
	return 0

score = 0
print("The max score is {}. Beegin!".format(max_score))
print_letters()
while True:
	put = input("{:03d} > ".format(score))
	try:
		if put == '\\letters':
			print_letters()
		elif put == '\\words':
			print_gotten()
		elif put == '\\hist':
			print_histogram()
		elif put == '\\hint':
			print_hint()
		elif put == '\\quit':
			break
		elif put.startswith('\\'):
			print("Unreccognized cummand.")
		else:
			score += get_word(put)
		if len(remaining) == 0:
			print()
			print("barke! ye got queen apid with {}/{} possible points!".format(score, max_score))
			break
	except Exception as e:
		print(e)
