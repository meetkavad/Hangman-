import random
import sqlite3
from tabulate import tabulate

HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''', '''
  +---+
 [O   |
 /|\  |
 / \  |
     ===''', '''
  +---+
 [O]  |
 /|\  |
 / \  |
     ===''']        

# Connect to the Hall Of Fame database i.e. HOF.db
conn = sqlite3.connect('HOF.db')
cursor = conn.cursor() # 

# Define SQL query to create a table
create_table_query = '''
CREATE TABLE IF NOT EXISTS highest_records (
    level VARCHAR(10) PRIMARY KEY,
    name TEXT NOT NULL,
    rem_lives INTEGER NOT NULL
)
'''

# Execute the SQL query to create the table
cursor.execute(create_table_query)
conn.commit()

# Check if the table is empty
cursor.execute("SELECT COUNT(*) FROM highest_records")
count = cursor.fetchone()[0]

# If the table is empty, insert the default records
if count == 0:
    insert_query = '''
    INSERT INTO highest_records 
    VALUES ('Easy', 'None', 0),
    ('Medium', 'None', 0),
    ('Hard', 'None', 0)
    '''
    cursor.execute(insert_query)
    conn.commit()
              
# Categories of words  : 
Animal  = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
Shape = 'square triangle rectangle circle ellipse rhombus trapezoid pentagon hexagon'.split()
Place = 'Cairo London Paris Baghdad Istanbul Riyadh Giza Thames Louvre Tigris Bosphorus Diriyah Luxor Thames Seine Euphrates Sultanahmet Najd Alexandria Soho Montmartre Green Galata Diriyah Sphinx Westminster'.lower().split()

def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def printIntro() : 
    # This function prints intro menu , allow user to choose level and categories.

    # To use the global variable HANGMAN_PICS locally
    global HANGMAN_PICS

    # create the introductory menu.
    table = [['Hello, ' + name + '! Let\'s play Hangman!'] , 
            ['PLAY THE GAME' + '\n' + '1. EASY \n2. MEDIUM \n3. HARD'],
            ['4. HALL OF FAME' ], 
            ['5. READ INSTRUCTIONS'] 
            ]
    
    # Take user input.
    while True : 
        print(tabulate(table , tablefmt='heavy_grid')) # Print introductory menu.
        print()
        choice = input()
        match choice : 
            case '1' : 
                level = 'Easy'
                category , secretWord = printCategory()  
                return (level , category , secretWord)
            case '2' : 
                level = 'Medium'
                HANGMAN_PICS = HANGMAN_PICS[:7] # Limit the trials to 6 by limiting the HANGMAN_PICS list length.
                category , secretWord = printCategory()
                return (level , category , secretWord)
            case '3' :
                level = 'Hard'
                HANGMAN_PICS = HANGMAN_PICS[:7]
                cat = random.choice([Animal , Shape , Place]) # Random selection of category.
                secretWord = getRandomWord(cat) 
                return (level,'',secretWord)
            case '4' : 
                printHOF()
            case '5' : 
                printInstructions()
            case _ :
                print("Please enter a number between 1 and 5.")

def printCategory() : 
    categoryTable = [['Select a Category'] , ['1. Animals\n2. Shapes\n3. Places']] 
    while True : 
        print(tabulate(categoryTable  , tablefmt='heavy_grid'))
        print()
        choice = input()
        match choice : 
            case '1' : 
                category = 'Animal'
                secretWord = getRandomWord(Animal)
                return (category , secretWord)
            case '2' : 
                category = 'Shape'
                secretWord = getRandomWord(Shape)
                return (category , secretWord)
            case '3' : 
                category = 'Place'
                secretWord = getRandomWord(Place)
                return (category , secretWord)
            case _ :
                print("please enter a number between 1 and 3")
            
def printHOF() : 
    # This function prints the hall of fame table.

    # Get HOF entries.
    cursor.execute("SELECT * from highest_records")
    row = cursor.fetchall()

    # Table to store hof entries.
    hofTable = [['HALL OF FAME'],['Level' , 'Name' , 'Lives Remaining'] ]

    # Store values in hofTable.
    for i in range(3) :
        hofTable.append([row[i][0] , row[i][1] , row[i][2]])

    print(tabulate(hofTable , tablefmt='heavy_grid'))
    print('Press Enter to continue')
    input()
    

def printInstructions() : 
    # This function prints the instruction table. 

    instructionTable = [['','ABOUT THE GAME '] , ['Easy', 'In this Level you will get a chance to select \na category of secret words. You will have 8\nlives to guess the correct word. '],
                        ['Medium', 'Similar to Easy level , in this Level as well you will get \na chance to select a category of secret words.\nYou will have 6 lives to guess the correct word. '],
                        ['Hard', 'In this Level a category of secret words will be randomly selected.\nYou will have 6 lives to guess the correct word. '], 
                        ['','Press Enter to go back to introductory menu'] , ['','Press \'e\' to exit the game']]
    
    while True : 
        print(tabulate(instructionTable , tablefmt='heavy_grid'))
        choice = input()  

        if choice == 'e':
            exit()
        else : 
            break
       
            
def displayBoard(category , missedLetters, correctLetters, secretWord):
    # This function prints the board.

    # Category get print if level is not Hard :
    if category : 
        print('Category: ' + category)

    print(HANGMAN_PICS[len(missedLetters)])
    print()
 
    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secretWord)

    for i in range(len(secretWord)): # Replace blanks with correctly guessed letters.
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks: # Show the secret word with spaces in between each letter.
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter and not something else.
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def updateScore(level , name , rem_lives) : 
    # This Function checks the high_score database for any updation once the game is over.

    # get the highest score from the database.
    get_highest_score_query = f'''
    SELECT * FROM highest_records WHERE level = '{level}'
    '''
    cursor.execute(get_highest_score_query)
    highest_score = cursor.fetchone()

    # if the player has beaten the highest score, update the database.
    if highest_score[1] == 'None' or rem_lives > highest_score[2]:
        update_score_query = f'''
            UPDATE highest_records SET 
            name = '{name}', rem_lives = '{rem_lives}'
            WHERE level = '{level}'
        '''
        cursor.execute(update_score_query)
        conn.commit()
        print('Congratulations! You have beaten the highest score.')

def playAgain():
    # This function returns True if the player wants to play again; otherwise, it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


print('H A N G M A N')

name = ''
missedLetters = ''
correctLetters = ''
secretWord = ''
category = ''
level = ''


# Take user name : 
print("Wait a minute! Who are You?")
while True :
    name = input()
    if not name : 
        print("please enter a name")
    else :
        break

level , category , secretWord = printIntro() 
gameIsDone = False

while True:

    displayBoard(category , missedLetters, correctLetters, secretWord)

    # Let the player enter a letter.
    guess = getGuess(missedLetters + correctLetters)

    if guess in secretWord:
        correctLetters = correctLetters + guess

        # Check if the player has won.
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('Yes! The secret word is "' + secretWord + '"! You have won!')

            # check and update the score in database.
            updateScore(level  , name , len(HANGMAN_PICS) - len(missedLetters))
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess

        # Check if player has guessed allowed number of trial times and lost.
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            displayBoard(category, missedLetters, correctLetters, secretWord)
            print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
            gameIsDone = True

    # Ask the player if they want to play again (but only if the game is done).
    if gameIsDone:
        if playAgain():

            name = ''
            missedLetters = ''
            correctLetters = ''
            secretWord = ''
            category = ''
            level = ''

            # Take user name again : 
            print("Hey are you the same guy?")
            ans = input()
            if not ans.lower().startswith('y') : 
                print("Then who are you?")
                while True :
                    name = input()
                    if not name : 
                        print("please enter a name")
                    else :
                        break
            else : name = name 

            level , category , secretWord = printIntro()
            gameIsDone = False

        else:
            conn.close() 
            break