from nltk.corpus import cmudict

d = cmudict.dict()
pre_dict = {}
suf_dict = {"tion":1, "uation":3}
add_dict = {}
hiatus = {}

def nsyl(word):
	return [len(list(y for y in x if y[-1].isdigit())) for x in d[word]]

def count_vowel(word):
	count = 0
	for w in word:
		if w in "aeiouy":
			count += 1
	return count

def count_consecutive_vowel(word):
	count = 0
	for n in range(len(word)-1):
		if word[n] in "aeiouy" and word[n+1] in "aeiouy":
			count += 1
	return count

def count_syllable(word):
	# lower
	word = word.lower()

	# prefix matching
	pre_flag = False
	for i in range(len(word)):
		try:
			pre_word = word[0:len(word)-i]
			if pre_word in add_dict:
				pre_syllable = add_dict[pre_word]
			elif pre_word in pre_dict:
				pre_syllable = pre_dict[pre_word]
			elif len(pre_word) <= 2:
				pre_syllable = count_vowel(pre_word)
				pre_flag = True
			else:
				pre_syllable = nsyl(pre_word)[0]
			#print(pre_word)
			break
		except:
			pass

	if i == 0:
		if pre_flag:
			c_vowel = count_consecutive_vowel(pre_word)
		else:
			c_vowel = 0	

		return pre_syllable - c_vowel
	else:
		# suffix matching
		suf_flag = False
		word = word[len(word)-i:]
		for j in range(i):
			try:
				suf_word = word[j:]
				if suf_word in add_dict:
					suf_syllable = add_dict[suf_word]
				elif suf_word in suf_dict:
					suf_syllable = suf_dict[suf_word]
				elif len(suf_word) <= 2:
					suf_syllable = count_vowel(suf_word)
					suf_flag = True
				else:
					suf_syllable = nsyl(suf_word)[0]
				#print(suf_word)
				break
			except:
				pass
	if j == 0:
		if pre_flag:
			if suf_flag:
				c_vowel = count_consecutive_vowel(pre_word + suf_word)
			else:
				c_vowel = count_consecutive_vowel(pre_word)
		
		else:
			if suf_flag:
				c_vowel = count_consecutive_vowel(suf_word)
			else:
				c_vowel = 0

		return pre_syllable + suf_syllable - c_vowel
	else:
		# middle matching
		word = word[0:j]
		#print(word)
		mid_syllable = count_vowel(word)
	
		# consecutive vowel
		if pre_flag:
			if suf_flag:
				c_vowel = count_consecutive_vowel(pre_word + word + suf_word)
			else:
				c_vowel = count_consecutive_vowel(pre_word + word)
		else:
			if suf_flag:
				c_vowel = count_consecutive_vowel(word + suf_word)
			else:
				c_vowel = count_consecutive_vowel(word)

		return pre_syllable + mid_syllable + suf_syllable - c_vowel
