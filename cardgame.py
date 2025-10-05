"""
BlackJack clone.
"""
import random
import arcade

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "BlackJack"

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The Y of the top row
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row
MIDDLE_Y = SCREEN_HEIGHT / 2

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The X of the middle row
MIDDLE_X = SCREEN_WIDTH / 2

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# If we fan out cards stacked on each other, how far apart to fan them?
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

# Constants that represent "what pile is what" for the game
PILE_COUNT = 3
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12

# Face down image
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up

        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = None

        self.background_color = arcade.color.AMAZON

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None
        
        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None
        
        # Create a list of lists, each holds a pile of cards.
        self.piles = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []
        
        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()
        
        # This makes the mat for the deck of cards (Index 0)
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, color = arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = SCREEN_WIDTH / 2, MIDDLE_Y
        self.pile_mat_list.append(pile)
        
        # This makes the mat for the computer player (Index 1)
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, color = arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = SCREEN_WIDTH / 2, TOP_Y
        self.pile_mat_list.append(pile)
        
        # This creates the players mat. (Index 2)
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, color = arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = SCREEN_WIDTH / 2, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create every card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = MIDDLE_X, MIDDLE_Y
                self.card_list.append(card)
                
        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)
            
        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
            
        # - Pull from that pile into the middle piles, all face-down
        # Deal proper number of cards for that pile
        for j in range(1,3):
            # Pop the card off the deck we are dealing from
            card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
            # Put in the proper pile
            self.piles[1].append(card)
            # Move card to same position as pile we just put it in
            card.position = self.pile_mat_list[1].position
            # Put on top in draw order
            self.pull_to_top(card)
            top_card = self.piles[1][-1]
            for i, dropped_card in enumerate(self.piles[1]):
                dropped_card.position = top_card.center_x + CARD_VERTICAL_OFFSET * (i), \
                                        top_card.center_y 
                
        # Flip up the top cards
        
        self.piles[1][-1].face_up()
        

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        
        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)
        
    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index
            
    def remove_card_from_pile(self, card):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break
            
    def move_card_to_new_pile(self, card, pile_index):
        """ Move the card to a new pile """
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            # Figure out what pile the card is in
            pile_index = self.get_pile_for_card(primary_card)

            if primary_card.is_face_down:
                # Is the card face down? In one of those middle 7 piles? Then flip up
                primary_card.face_up()
            else:
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [primary_card]
                # Save the position
                self.held_cards_original_position = [self.held_cards[0].position]
                # Put on top in drawing order
                self.pull_to_top(self.held_cards[0])

                # Is this a stack of cards? If so, grab the other cards too
                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_position.append(card.position)
                    self.pull_to_top(card)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # What pile is it?
            pile_index = self.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # Is it on a middle play pile?
            elif PLAY_PILE_1 <= pile_index <= PLAY_PILE_7:
                # Are there already cards there?
                if len(self.piles[pile_index]) > 0:
                    # Move cards to proper position
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x + CARD_VERTICAL_OFFSET * (i + 1), \
                                                top_card.center_y 
                else:
                    # Are there no cards in the middle play pile?
                    for i, dropped_card in enumerate(self.held_cards):
                        # Move cards to proper position
                        dropped_card.position = pile.center_x + CARD_VERTICAL_OFFSET * i, \
                                                pile.center_y

                for card in self.held_cards:
                    # Cards are in the right position, but we need to move them to the right list
                    self.move_card_to_new_pile(card, pile_index)

                # Success, don't reset position of cards
                reset_position = False

            # Release on top play pile? And only one card held?
            elif TOP_PILE_1 <= pile_index <= TOP_PILE_4 and len(self.held_cards) == 1:
                # Move position of card to pile
                self.held_cards[0].position = pile.position
                # Move card to card list
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)

                reset_position = False

        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy
            
    def on_key_press(self, symbol: int, modifiers: int):
        """User presses key"""
        if symbol == arcade.key.R:
            # Restart
            self.setup()
        elif symbol == arcade.key.H:
            # Hold
            self.hold()
            
    def convert_card_value(self, card_value: str, total: int) -> int:
        """Return blackjack numeric value for a card string.

        Args:
            card_value: One of the strings in CARD_VALUES (e.g. 'A', '2', ..., '10', 'J').
            total: Current total for the hand; used to decide whether Ace should be 11 or 1.

        Returns:
            Integer value of the card in blackjack.
        """
        # Face cards and 10 all count as 10
        if card_value in ["K", "Q", "J", "10"]:
            return 10

        # Ace can be 11 or 1. Prefer 11 if it doesn't bust the hand.
        if card_value == "A":
            return 11 if total + 11 <= 21 else 1

        # Numeric cards: just convert to int (values are '2'..'9')
        try:
            return int(card_value)
        except ValueError:
            # Fallback: if something unexpected is passed, treat as 0
            return 0
            
    def hold(self):
        """Hold logic"""
        # Count held cards for dealer
        
        # While loop until total card pile value is >= 17
        # Recompute total each iteration, draw from the deck (pile 0) until >= 17
        for card in self.piles[1]:
                card.face_up()
        while True:
            total = 0
            for card in self.piles[1]:
                total += self.convert_card_value(card.value, total)

            if total >= 17:
                break

            # Dealer should draw: take top card from the face-down deck (pile 0)
            if len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                # No cards left to draw
                break

            # Pop from deck, put into dealer's pile (pile 1), face up and pull to top
            card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
            self.piles[1].append(card)
            card.position = self.pile_mat_list[1].position
            card.face_up()
            self.pull_to_top(card)
            top_card = self.piles[1][-1]
            for i, dropped_card in enumerate(self.piles[1]):
                dropped_card.position = top_card.center_x + CARD_VERTICAL_OFFSET * (i), \
                                        top_card.center_y 
            

def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
