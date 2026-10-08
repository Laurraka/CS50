import itertools
import random

HEIGHT = 8
WIDTH = 8
MINES = 8


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=HEIGHT, width=WIDTH, mines=MINES):

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
        if len(self.cells)==self.count:
            return set(self.cells)
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return set(self.cells)
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count=self.count-1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
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
        i, j= cell
        if not (0<=i<HEIGHT and 0<=j<WIDTH):
            return ValueError

        # Marks cell that has been clicked
        self.moves_made.add(cell)
        
        # Marks cell as safe
        self.mark_safe(cell)

        # Add sentence given by the number of mines within the neighboring cells
        new_info=Sentence(set(), count) 

        for ii in range(i-1, i+2):
            for jj in range(j-1, j+2):
                if 0<=ii<self.height and 0<=jj<self.width:
                    if (i,j)==(ii,jj):
                        continue

                    if (ii,jj) in self.mines:
                        new_info.count-=1
                        continue

                    if (ii,jj) in self.safes:
                        continue

                    new_info.cells.add((ii,jj))

        self.knowledge.append(new_info)

        knowledge_changed=True

        while knowledge_changed:

            knowledge_changed=False
            
            mines=set()
            safes=set()

            for sentence in self.knowledge:
                mines=mines|sentence.known_mines()
                safes=safes|sentence.known_safes()
            
            for m in mines-self.mines:
                self.mark_mine(m)
                knowledge_changed=True

            for s in safes-self.safes:
                self.mark_safe(s)
                knowledge_changed=True

            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]       

            # Mark new safe cells inferred by AI's knowledge
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s2.cells<s1.cells and len(s1.cells-s2.cells)==1 and s1.count==s2.count:
                        diff = s1.cells - s2.cells
                        (cell,) = diff
                        
                        if cell not in safes:
                            knowledge_changed=True
                            self.mark_safe(cell)

            # Mark new mines inferred by AI's knowledge
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s2.cells<s1.cells and len(s1.cells-s2.cells)==1 and s1.count-1==s2.count:
                        diff = s1.cells - s2.cells
                        (cell,) = diff
                        
                        if cell not in mines:
                            knowledge_changed=True
                            self.mark_mine(cell)

            # Add new sentences
            new_sentences=[]
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s2.cells<s1.cells and len(s1.cells-s2.cells)>1 and (Sentence(s1.cells-s2.cells, s1.count-s2.count) not in new_sentences):
                        unknown_set=set()
                        unknown_count=s1.count-s2.count

                        for cell in s1.cells-s2.cells:
                            if cell in self.mines:
                                unknown_count-=1
                            
                            if cell not in self.mines and cell not in self.safes:
                                unknown_set.add(cell)
                        
                        if len(unknown_set)!=0:
                            knowledge_changed=True
                            new_sentences.append(Sentence(unknown_set, unknown_count))

            self.knowledge=self.knowledge+new_sentences

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_moves=self.safes-self.moves_made

        if possible_moves==set():
            return None
        else:
            return random.choice(list(possible_moves))

        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Initialize an empty field
        board = set()
        for i in range(self.height):
            for j in range(self.width):
                board.add((i,j))

        forbidden=self.moves_made.union(self.mines)

        possible_moves=board-forbidden

        if possible_moves==set():
            return None
        else:
            return random.choice(list(possible_moves))