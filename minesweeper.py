import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # Checking if the count is equal to the length of the cells, if so they are all mines.
        if self.count == len(self.cells) and self.count:
            return self.cells
        
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Checking if the count is empty, if so they are all safes.
        if not self.count:
            return self.cells
        
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Checking if a cell is in a sentence, if so remove it and change the count.
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Checking if a cell is in a sentence, if so remove it.
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1)
        self.moves_made.add(cell)
        
        # 2)
        self.mark_safe(cell)
        
        # 3)
        # Initializing a set to keep track of new sentence cells.
        neighbors = set()
        
        # Creating the cells of the new sentence.
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Checking if the cell is already a known safe.
                if (i, j) in self.safes:
                    continue
                
                # Checking if the cell is already a known mine.
                if (i, j) in self.mines:
                    count -= 1
                    continue
                
                if i in range(0, self.height) and j in range(0, self.width):
                    neighbors.add((i, j))
        
        # Creating new sentence and adding it to the knowledge base.
        self.knowledge.append(Sentence(neighbors, count))
        
        # Creating a new_data variable to keep track of new sentences and new safe cells or mines.
        new_data = True
        while new_data:
            # Setting new_data as False until new information appears.
            new_data = False
            
            # 4)
            # Getting additional info from the sentences in the knowledge base.
            mine_cells = set()
            safe_cells = set()
            for sentence in self.knowledge:
                mine_cells = mine_cells.union(sentence.known_mines())
                safe_cells = safe_cells.union(sentence.known_safes())
            
            # Marking new mine_cells or safe_cells, if any.
            if mine_cells:
                for mine in mine_cells:
                    self.mark_mine(mine)
                new_data = True
            if safe_cells:
                for safe in safe_cells:
                    self.mark_safe(safe)
                new_data = True
            
            # Removing empty sentences from the knowledge base. Empty sentences
            # are created when known_safes or known_mines make changes to the sentences.
            self.knowledge = [sentence for sentence in self.knowledge if sentence != Sentence(set(), 0)]
            
            # 5)
            # Looping through every combination of sentences and creating new sentences.
            for sentence_1, sentence_2 in itertools.permutations(self.knowledge, 2):
                if sentence_1.cells.issubset(sentence_2.cells):
                    new_sentence = Sentence(sentence_2.cells - sentence_1.cells, sentence_2.count - sentence_1.count)
                    
                    # Checking if the new sentence is already in the knowledge base.
                    if new_sentence not in self.knowledge:
                        self.knowledge.append(new_sentence)
                        new_data = True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Creating a set of the safe moves, then making a random choice.
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return random.choice(list(safe_moves))
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            # Generating the next random move.
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            
            # Checking if the move has already been made or if it is a known mine.
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return (i, j)
