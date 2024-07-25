import re
import os
import random
import time
# TODO: max length


class GenEffect():
    def __init__(self):
        self.chosen_pointers = None
        self.file = "words.txt"
        self.log = "log.txt"
        self.worddict = {}
        self.pointer = 0
        # TODO: max length
        self.used_pointers = []
        self.openwords()
        self.openlog()

    def openwords(self):
        with open(self.file, "r") as f:
            for count, line in enumerate(f):
                pattern = re.compile(r'(.+?)\t(.+?)\n')
                matches = pattern.findall(line)

                for match in matches:
                    word, translation = match
                    self.worddict[count] = [word, translation]

    def openlog(self):
        with open(self.log, "r") as f:
            self.pointer = int(f.readline())

    def choose_pointers(self):
        # TODO: 0 pointer - 2
        self.chosen_pointers = [x for x in range(self.pointer - 2, self.pointer + 8)]

        # Add extra question from previously learned
        chosen_old_question = int()
        for i in range(2):
            if self.pointer > 20:
                while True:
                    random_choice = random.randint(0, self.pointer - 20)
                    if random_choice == chosen_old_question:
                        continue
                    else:
                        self.chosen_pointers.append(random_choice)
                        chosen_old_question = random_choice
                        break
        print("\n")

    def geneffect(self):

        while True:
            questions_orig_number = int()
            questions_new_number = int()
            os.system("clear")
            self.choose_pointers()

            while True:
                os.system("clear")

                # Print learning list, but don't show the two extra questions
                for key in self.chosen_pointers:
                    if self.worddict[key] == self.worddict[self.chosen_pointers[10]]:
                        break
                    out = self.worddict[key]
                    print("{: >10} {: >20}".format(*out))

                input("\n\nEnter to start practice.")
                os.system("clear")

                # Choose word to be asked
                while True:
                    rand_pointer = random.choice(self.chosen_pointers)
                    if rand_pointer not in self.used_pointers:
                        question = (self.worddict[rand_pointer][0])
                        questions_orig_number = rand_pointer
                        break

                # How many blank lines
                if len(question) <= 3:
                    hide = 1
                elif 3 < len(question) < 5:
                    hide = 2
                else:
                    hide = int(abs(len(question) * 0.5))

                # Select letters to be removed
                choises = [x for x in range(len(question))]
                print("choices", choises)
                for joker in range(hide):
                    choises.remove(random.choice(choises))

                # Put "_" in new word
                new_question = ""
                for index, char in enumerate(question):
                    if index in choises:
                        new_question += char + ""
                    else:
                        new_question += " _ "
                print(new_question, "\n")

                # Print translation alternatives
                # Make new indexes 1-10, register original number of right answer
                shown_alternatives = []
                for x in range(0, 10):      # 1, 11
                    shown_alternatives.append(random.randint(0, len(self.worddict)-1))

                random_number = random.randint(0, 9)

                # Put right answer in the list
                shown_alternatives[random_number] = questions_orig_number

                # Print alternatives
                for index, key in enumerate(shown_alternatives):

                    try:
                        print(index, ": ", self.worddict[key][1]) # +1
                    except KeyError:
                        print(index, key)
                    if self.worddict[key][1] == self.worddict[questions_orig_number][1]:
                        questions_new_number = index # +1

                # Ask and test
                fails = 0
                while True:
                    # Guess the word
                    if fails >= 3:
                        break
                    try:
                        answer_word = input("\nWrite the word: ")
                        if answer_word == question:
                            print("\nYES!!!\n")
                            break
                        else:
                            print("\nNO!!!!\n")
                            fails += 1

                    except ValueError:
                        print("Wrong input type!!")

                # Choose translation
                while True:
                    if fails >= 3:
                        break
                    try:
                        answer_translation = input("Choose translation: ")
                        if int(answer_translation) == questions_new_number:
                            print("\nYES!!!\n")
                            break
                        else:
                            print("\nNO!!!!\n")
                            fails += 1

                    except ValueError:
                        print("\nNO!!!!\n")
                time.sleep(1)

                if fails >= 3:
                    fails = 0
                    print("Right answer: ", question, rand_pointer)
                    time.sleep(2)
                    continue

                self.used_pointers.append(rand_pointer)

                if len(self.used_pointers) >= 12:
                    self.pointer += 8
                    self.used_pointers = []
                    print("\nNEW ROUND.\n")
                    with open(self.log, "w") as f:
                        f.write(str(self.pointer))
                    print("\nWords learned: ", self.pointer)
                    time.sleep(2)
                    break


#TODO: Some answer alternatives can be the same name

geneffect = GenEffect()
geneffect.geneffect()
