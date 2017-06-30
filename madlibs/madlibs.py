import random

"""Questions for each level are stored in lists.
Adding additional questions to the quiz is as easy as adding items to a list!
"""


easyQuestions = ['''\nA ___1___ lives on a farm and gives us beef and milk. A ___1___ goes moo.
    \nAlso on the farm is another animal that makes milk: the ___2___. The ___2___ doesn't moo but instead bleats!
    \nFinally, their friends the ___3___ goes baaaah. ___3___ are shaved to give us ___4___!''', '''
    \nThe ___1___ Ocean is the largest body of water on earth.
    \nThe ___2___ Ocean separates North America and Europe.
    \nIf you sailed from Australia to Africa you'd probably cross the ___3___ Ocean.
    \nTake a coat if you visit the ___4___ Ocean!''']

mediumQuestions = ['''\nThe ___1___ is the only mammal that can fly. They are considered ___2___ because they are primarily active at night.
    \nThe fastest flyer in the sky is the ___3___ falcon. They can reach speeds over 200 ___4___!
    \nSpeed is not everything, though. The Alpine ___5___ can stay aloft for over 200 consecutive days! That's a record!''']

hardQuestions = ['''\nChoosing between the number one or two, I'd select ___1___.
    \nA number between one and five? ___2___ of course.
    \nOne and ten? ___3___.
    \nAny number??? I'd obviously choose ___4___.''']

"""Answers are also stored in lists."""

easyAnswers = [["cow", "goat", "sheep", "wool"], ["pacific", "atlantic", "indian", "arctic"]]

mediumAnswers = [["bat", "nocturnal", "peregrine", "mph", "swift"]]

hardAnswers = [[str(random.randint(1,2)), str(random.randint(1,5)), str(random.randint(1,10)), str(random.random()*1000)]]

def fill(answer, question, number):
    """ Updates question with most recent answer filled in"""
    return question.replace("___" + str(number+1) + "___", answer)

def evaluate(response, answer):
    """ Compares user's response to the stored answer.
    
    response is user input; answer is pulled from appropriate list.
    'correct' variable remains False until user provies correct response
    If user gets it wrong 3 times they'll be given the answer, but we don't tell them this!
    """
    correct = False
    r = 2 # remaining tries
    while not correct:
        if response.lower() == answer and r == 2:
            print("\nWow, nice work! You got it on the first try!")
            correct = True
        elif response.lower() == answer and r != 2:
            print("\nNice work, you got it!")
            correct = True
        elif r == 0:
            print("\nOh no! You missed 3 in a row. We filled in the answer for you. Keep trying!")
            break
        else:
            response = input("\nWhoops! You have " + str(r) + " attempt left. Try again: ")
            r -= 1

def quiz(question, answer):
    """ Prompts user with question from appropriate level and directs their response to appropriate functions

    First loop will run for each question in the list.
    The question is pulled and stored as a variable so that it can be updated in the next loop

    Second loop takes in user input and compares it, using the evalute function, against correct answer.
    Once user answers, the question is updated with blank filled in and given to user again.

    User receives small congratulation when they fill in all blanks for a question,
    and a big congratulation once they've completed all questions.

    """
    for q in range(0, len(question)):
        print(question[q])
        que = ""
        que = question[q]
        for a in range(0, len(answer[q])):
            userInput = input("\nWhat is your answer for ___" + str(a+1) + "___? ")
            evaluate(userInput, answer[q][a])
            que = fill(answer[q][a], que, a)
            print(que)
        print("*** You finished the question! ***")
    print('''
    \n  *                    *
    \n ***    Great work!   ***
    \n*****                *****
    \n ***   You finished!  ***
    \n  *                    *
    \n ''')

def difficulty():
    """ Program will loop until run variable is turned to False"""
    run = True
    while run:
        """ Prompt user to select level of difficulty.
        Response will determine which questions they're asked.
        """
        print('''*** Get ready for a quiz! ***
        \n
        \nHow smart are you feeling?
        \n1. What's a compuderp?
        \n2. Feeling pretty good!
        \n3. Get on with the quiz you're wasting my time
        \n0. Nevermind I don't want to play.''')
        level = input("Enter a number: ")
        """As long as response includes a single valid number they'll proceed.
        A response that contains 0 or 'q' (e.g. Quit) will end the program.

        Depending on response, appropriate level of questions/answers will be used
        """
        if level.find("1") != -1:
            print("\nGood work! You've been put into the easy level.\nDon't worry, I'll talk slow.\nHere's the first question. Take your time, this is a judgment free zone.\n\n\n")
            quiz(easyQuestions, easyAnswers)
        elif level.find("2") != -1:
            print("\nGlad to hear you're doing well; we're on the medium track!\nYou have 3 chances to answer each question!\nHere's the first one. You've got this!\n\n\n")
            quiz(mediumQuestions, mediumAnswers)
        elif level.find("3") != -1:
            print("\nOK smarty pants. Let's see how smart you really are!\nGloves off!")
            quiz(hardQuestions, hardAnswers)
        elif level.find("0") != -1 or (level.lower()).find("q") != -1:
            print("Goodbye!")
            run = False
        else:
            print('''Sorry, you failed the quiz. Try again!
            \n(Next time try entering a NUMBER)''')

""" Run the program!"""
difficulty()
