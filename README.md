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

### Key Algorithms
1. **Puzzle Generation**:
   - Selects a random 6-letter main word
   - Finds all valid subwords (3-6 letters) from the main word
   - Places words in a grid with intersections and buffers
   - Validates grid has sufficient words (≥21)

2. **Word Validation**:
   - Checks if a word can be formed from the main word's letters
   - Verifies word length (3-6 letters)
   - Ensures word isn't the main word itself

3. **Grid Placement**:
   - Main word is placed diagonally
   - Other words intersect with main word or existing words
   - Maintains proper buffers around words

## Testing

### Unit Tests
The project includes pytest unit tests that verify:
- Word validation logic
- Grid generation constraints
- Game state updates
- Scoring calculations

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
1. Create a new test file or add to existing ones
2. Follow pytest naming conventions (`test_*.py` files, `test_` prefix for functions)
3. Focus on one specific functionality per test
4. Include both positive and negative test cases

## Bonus Features

1. **Multiple Difficulty Levels**:
   - 5 distinct levels with varying lives (3-20)
   - Clear progression system (Apprentice to Elder)

2. **Interactive Menus**:
   - Beautifully formatted terminal interface
   - Color-coded options and status displays
   - Smooth navigation between screens

3. **Game Mechanics**:
   - Word shuffling feature
   - Dynamic scoring based on revealed letters
   - Visual distinction between main word and other words

4. **Enhanced UX**:
   - Clear game state display (lives, points, last guess)
   - Help manual with detailed instructions
   - Animated screen transitions

5. **Advanced Puzzle Generation**:
   - Intelligent word placement algorithm
   - Guaranteed minimum word count
   - Valid intersection checking
