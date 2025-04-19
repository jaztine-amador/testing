

# Wizards of Worderly Place
Welcome to the Worderly Place! A place that will test your wizardry in uncovering the mysterious words hidden beneath the magical word puzzle!





## User Manual

### How to Run the Game
1. Make sure Python 3 is installed
2. Install the dependencies of the program.
    - `python3 -m pip install -r requirements.txt`
3. Initialize the game
    - Without lexicon file: `python3 main.py`
    - With lexicon file: `python3 main.py your_lexicon_file.txt`

### Game Controls
- **Guess a Word**: Type any word guess and press `Enter`
- **Shuffle Letters**: Type `S` and press `Enter` to rearrange the available letters
- **Exit Game Level**: Type `E` and press `Enter` to exit the game level

### Game Mechanics
- The game starts with a set of scrambled letters from the 6-letter main word.
- The puzzle grid shows the arrangement of 21 hidden words (3-6 letters long) made of these letters.
- The player is tasked to find / guess all the hidden words.
- Each correct guess reveals the placement of the word in the puzzle grid.
  - A guess is correct if it is in the puzzle grid and is still hidden.
- The player will earn a point for every new letter revealed.
- The game will end in any of the following conditions:
  - All hidden words in the puzzle grid are revealed.
  - All lives have been consumed.
  - The player has quit the game level.

### Main Menu
- **Select Game Level**: Type `P` and press `Enter` to open the Game Level Menu
- **Read User Manual**: Type `H` and press `Enter` to open the Help Menu
- **Exit Game**: Type `E` and press `Enter` to exit the game

### Help Menu
- **Exit to Main Menu**: Press `Enter` to return to the Main Menu

### Game Level Menu
- **Initialize a game level**: Type `game_level` and press `Enter` to play the game level
- **Exit to Main Menu**: Type `E` and press `Enter` to return to the Main Menu







## Code Organization

### File Structure
- **`main.py`**: Handles command line arguments
- **`game_logic.py`**: Handles puzzle grid generation and core game mechanics
- **`main_menu_display.py`**: Handles all display menus and navigation
- **`utilities.py`**: Contains all the helper functions
- **`requirements.txt`**: Contains the dependencies of the program
- **`ac-permanent-lexicon.txt`**: The permanent lexicon file of the program

### Key Algorithms
1. **Puzzle Grid Generation**
   - Randomly selects a 6-letter main word from the list of words
   - Finds all valid subwords (3-6 letters long) of the main word from the list of words
   - Sorts the list of valid words by decreasing length to prioritize the placement of longer words, creating more intersection points in the puzzle grid
   - Places the main word diagonally at the center of the grid
   - Intersects a valid word on each character of the main word
   - Intersects a valid word on any character in the puzzle grid
     - **Remarks**: Each word that is intersected / placed on the grid once is removed from the list of valid words, ensuring a word only appears once in the puzzle grid
   - Verifies whether the generated puzzle grid is valid
   - Continuously generates a puzzle grid until a valid one is produced

2. **Intersection Validation**
   - Verifies whether a word can be placed starting from a certain cell (i, j) such that;
      - It intesects at least one letter of another word in the puzzle grid
      - It does not intersect with another word of the same orientation
      - If oriented horizontally, there is no other horizontally oriented word one cell above and below it, no vertically oriented word has its first letter one cell below it, and no vertically oriented word has its last letter one cell above it
      - If oriented vertically, there is no other vertically oriented word once cell at the right and left side of it, no horizontally oriented word has its first letter one cell at the right side of it, and no horizontally oriented word has its last letter one cell at the left side of it
   - Prioritizes horizontal intersection given that the puzzle grid has more columns than rows, creating more intersection points in the puzzle grid

3. **Game Player**
   - Initializes the game given a puzzle grid, main word, all valid guess, and lives
   - Verifies whether the game continues or terminates
      - If not all words in the puzzle grid has been revealed and not all lives has been consumed, the game will continue
      - Otherwise, the game will terminate
   - Repeats a set of actions until the game ends
      - Displays the latest state of the game, which includes the updated puzzle grid, jumbled letters, lives, points, and the latest guess of the player
      - Prompts the player for their guess / command
      - Validates the input of the player
       - Updates corresponding variables in the game based on the validation
   -  Displays the final state of the game
   -  Displays a message based on the result of the game
   -  Prompts the player to exit to the Game Level Menu

4. **Guess Validation**
   - Verifies whether the player's guess is valid based on the following conditions:
      - It is a word in the puzzle grid
      - It was not revealed in the puzzle grid through previous guesses
   - Utilizes the list of valid guess and the pointing system of the game

5. **Grid Update**
   - Updates the puzzle grid once the player's guess has been validated
   - Determines the orientation of the word in the puzzle grid
   - Collects all the cells ( i , j ) that is occupied by the letters of the word
   - Conditionally updates the characters in the grid
      - If the letter at the cell is still hidden, meaning it is still represented as the character "#", then it is replaced by the corresponding letter
      - If the cell is located at the main diagonal, meaning the letter located at it belongs to the main word, then it is replaced by the corresponding letter in upper case
      - Otherwise, it is replaced by the corresponding letter in lower case
   - Otherwise, no changes is applied to the cell


6. **Points Computation**
   - Calculates the points gained by the player given a valid guess
      - A guess will not gain a point if and only if it is already revealed in the puzzle grid through previous guesses
      - Based on the implementation of puzzle grid generation, a valid guess not gaining a point can only happen for the main word and the words intersecting it







## Testing

### Unit Tests
The project includes pytest unit tests that verify:
1. **Grid Generation**
   - Tests whether the grid generated is valid:
      - Checks whether the words are hidden before playing the game
      - Checks whether there are at least 20 valid words/guesses in the puzzle
      - Checks whether the main word is of length 6 and can be found in the main diagonal
   - Tests whether the word is placed properly in the grid.
      - Checks whether there is a buffer before placing a word in the grid
      - Checks whether it is possible to place the word in the grid (no overlapping)
2. **Word Generation**
   - Tests whether the words generated are valid
      - Checks whether the main word selected is always of length 6
      - Checks whether at least 20 valid guesses are generated
      - Checks whether the "guesses" generated are valid
3. **Scoring Updates**
   - Tests whether the game is updating the scores properly
   - Scores should be updated depending on how many words are revealed in the grid

### Running Tests
1. Install pytest if not already installed:
   `pip install pytest`
2. Run tests:
   `python3 -m pytest`

### Test Coverage
Tests are reasonably thorough because they:
- Cover all major game functions
- Include edge cases (minimum/maximum word lengths)
- Verify proper error handling
- Test both valid and invalid inputs

### Adding New Tests
1. Adding New Test Functions
   - Follow the naming conventions (`test_*.py` files, `test_` prefix for functions)
   - Focus on one specific functionality per test
   - Include both positive and negative test cases
2. Adding New Test Cases
   - Follow the assertion conventions
   - It is advisable to use the pre-existing main cases, to ensure proper assertions
   - Using an arbitrary main word may not ensure proper assertions in the placement of each words









## Bonus Features

1. **Display Menus**
   - Main Menu
      - Acts as the main page of the game
      - Displays other menus that the player can navigate and explore
   - Game Level Menu
      - Displays the difficulty levels of the game
      - Allows players to initialize and play the game at certain difficulty
      - Allows players to continue playing the game without running it in the terminal again
   - Help Menu
      - Acts as the player's manual of the game
      - Display information about the mechanics, pointing systen, and difficulty levels of the game

2. **Multiple Difficulty Levels**
   - Allows players to play the game at a specific difficulty
   - Five (5) distinct levels with varying maximum lives and themed progression system
      - `Apprentice`: 20 Lives      ( Easiest )
      - `Scholar`: 15 Lives
      - `Sorcerer`: 10 Lives
      - `Master`: 5 Lives
      - `Elder`: 3 Lives            ( Hardest )

3. **Word Shuffle Feature**
   - Allows the players to shuffle the provided letters in the game
   - Aids players in making guesses from the given letters

4. **Exit Feature**
   - Game Exit
      - Allows players to exit a certain game level and return to the game level menu
   - Program Exit
      - Allows players to exit the program from the main menu

5. **Colored Terminal Text**
   - Display and highlights important details of the game based on their functionality and their relevance to the the theme

6. **Permanent Lexicon File**
   - Allows players to run the program and play game without an input lexicon file


