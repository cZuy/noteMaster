# NoteMaster
# Prompts the user to create a journal entry - to track ideas and for later reference

import datetime as dt
from difflib import SequenceMatcher

# Welcome text (colorized)
# ANSI exit codes (\033) enable text color changing 1 for style (bold), 36 for color (cyan), 4 (black background), 0 to cancel, m to finish
print('''
\033[1;36;40mWelcome to NoteMaster!\033[0;36;49m
Just type a note and hit enter to get started.
To end your session, type \"exit\".
Tip: Multiple contexts/keywords can be entered by separating them with commas.\033[0m''')

file = open('journal.txt', 'r') # Brings in historical journal entries

journalOldLines = [] # Stores the existing journal as a list, separated by lines
journalOldWords = [] # Stores the existing journal as a list, separated by words

# Converts the .txt file to a list
for line in file:
	stripped_line = line.strip()
	line_list = stripped_line.split()
	journalOldLines.append(stripped_line)
	journalOldWords.append(line_list)

file = open('journal.txt', 'a+') # Allows adding entries to the journal
journalNew = [] # List for storing journal entries created in the current session
context = ''

# Compares similarity of strings - find past journal entries that are relevant to what's being typed now
def similar(a,b):
	return SequenceMatcher(None,a,b).ratio()

if __name__ == '__main__':  # Allows the program to run repeatedly
	while True:
		entry=input("\n\033[1;36;49mNote:         \033[0m") # Prompts user to create a new note
		if entry.lower() == 'exit': # Session will end if the use types "exit" (case insensitive)
			break
		entry2=input("\033[1;36;49mContext(s):   \033[0;33;49m%s\tChange?:      \033[0m" % context) # Shows current context and allows user to change context(s)
		if entry2 != '': # Previous context will be maintained if the user makes no change
			context = entry2
		entry3=input("\033[1;36;49mKeyword(s):   \033[0m") # Prompts user to enter keyword(s) for the new note
		now=dt.datetime.now()
		journal_entry=str(now)+' '+entry+' CONTEXT: '+context+' KEYWORDS: '+entry3 # Adds time, context, and keywords to the new note
		journalNew.append(journal_entry) # Adds new note to the python list
		file.write(journal_entry+'\n') # Writes new note to the text file
		similarityRatio = 0.0
		similarityLine = ''
		# Compares the similarity of the current note with the entries in the journal when the app was opened
		# Displays the most similar result
		# Needs adjustment for string length, it misses obvious matches
		for i in range(len(journalOldLines)):
			ratioTest = similar(journal_entry.partition(' ')[2].partition(' ')[2],journalOldLines[i].partition(' ')[2].partition(' ')[2].partition(' CONTEXT: ')[0])
			if ratioTest>similarityRatio:
				similarityRatio=ratioTest
				similarityLine=journalOldLines[i]
		print('\033[1;36;49mSimilar Note: \033[0;33;49m'+similarityLine.partition(' ')[2].partition(' ')[2].partition(' CONTEXT: ')[0]+"\033[0m") # Prints most similar journal entry

# Prints notes that were created in the current session without timestamps
print('\n\033[1;36;49mNew Notes:\033[0m')
for i in range(len(journalNew)):
	print(journalNew[i].partition(' ')[2].partition(' ')[2])

# Consider removing/reducing weight of non-descriptive words. ex. "the"
# Rank words and phrases by descriptiveness, common words will be lower
# Add the ranking score of matched words between the note entered and each line or group of notes
# Possibly adjust for long sentences
# Consider synonym strength
# Later, add tools to analyze notes
