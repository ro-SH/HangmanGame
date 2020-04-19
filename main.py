import pygame
from random import randint
from tkinter import messagebox, Tk

WIDTH = 500
HEIGHT = 500
DISPLAY = (WIDTH, HEIGHT)

BG_COLOR = (0, 0, 0)
MENU_TEXT_COLOR = (255, 0, 0)
MENU_BUTTON_COLOR = (0, 0, 0)
MENU_BUTTON_EXTRA_COLOR = (217, 195, 195)
MAIN_GAME_COLOR = (102, 255, 0)
ALPHABET_EXTRA_COLOR = (255, 255, 255)

MAIN_FONT = 'comicsans'
MAIN_FONT_SIZE = 30

MAIN_BUTTON_WIDTH = 200
MAIN_BUTTON_HEIGHT = 60
ALPHABET_BUTTON_WIDTH = 38
ALPHABET_BUTTON_HEIGHT = 38
LINE_WIDTH = 3

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

HANGMAN = [pygame.image.load(f'sprites/Hangman/Hangman{i}.png') for i in range(7)]
TICK = pygame.image.load('sprites/tick.png')
CROSS = pygame.image.load('sprites/cross.png')

playing = False

guessing_word = 'testttst'.upper()
guessed = '_' * len(guessing_word)
mistakes = 0
guessed_letters = []

class Button:

    def __init__(self, x, y, width, height, color, outline=None, text='', text_color=BG_COLOR, font=MAIN_FONT, font_size=MAIN_FONT_SIZE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.outline = outline
        self.text = text
        self.text_color = text_color
        self.font = font
        self.font_size = font_size

    def draw(self, win):
        if self.outline:
            pygame.draw.rect(win, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text:
            font = pygame.font.SysFont(self.font, self.font_size)
            text = font.render(self.text, 1, self.text_color)
            win.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + self.height // 2 - text.get_height() // 2))

    def is_over(self, pos):
        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                return True

        return False

play_button = Button(WIDTH // 2 - MAIN_BUTTON_WIDTH // 2,
    HEIGHT // 2 - 10 - MAIN_BUTTON_HEIGHT,
    MAIN_BUTTON_WIDTH,
    MAIN_BUTTON_HEIGHT,
    MENU_BUTTON_COLOR,
    MENU_TEXT_COLOR,
    'PLAY',
    MENU_TEXT_COLOR,
    MAIN_FONT,
    MAIN_FONT_SIZE
    )

quit_button = Button(WIDTH // 2 - MAIN_BUTTON_WIDTH // 2,
    HEIGHT // 2 + 10,
    MAIN_BUTTON_WIDTH,
    MAIN_BUTTON_HEIGHT,
    MENU_BUTTON_COLOR,
    MENU_TEXT_COLOR,
    'QUIT',
    MENU_TEXT_COLOR,
    MAIN_FONT,
    MAIN_FONT_SIZE
    )

alphabet_buttons = [Button(19 + index % 9 *(15+ALPHABET_BUTTON_WIDTH), HEIGHT - (ALPHABET_BUTTON_HEIGHT + 15) * (3 - index // 9), ALPHABET_BUTTON_WIDTH, ALPHABET_BUTTON_HEIGHT,
    BG_COLOR, MAIN_GAME_COLOR, letter, MAIN_GAME_COLOR, MAIN_FONT, MAIN_FONT_SIZE)
for index, letter in enumerate(ALPHABET)]

result = {
    True: f'You\'ve won!!! Congratulations!!!\nThe word was {guessing_word}.\nWould you like to play again?',
    False: f'You\'ve lost.\nThe word was {guessing_word}.\nWould you like to play again?'
}


def start_new_game():
    global guessing_word
    global guessed
    global mistakes
    global guessed_letters

    guessing_word = 'testests'.upper()
    guessed = '_' * len(guessing_word)
    mistakes = 0
    guessed_letters = []


def end_game(win, victory):
    global playing
    draw_main_window(win)
    Tk().wm_withdraw()
    answer = messagebox.askyesno('Game Over', result[victory])
    if answer:
        start_new_game()
    else:
        playing = False

def draw_main_window(win):

    win.fill(BG_COLOR)
    if playing:
        font = pygame.font.SysFont(MAIN_FONT, MAIN_FONT_SIZE)
        text = font.render(f'Guess the word ({len(guessing_word)} symbols)', 1, MAIN_GAME_COLOR)
        win.blit(text, (WIDTH // 2 - (text.get_width() // 2), 10))

        win.blit(HANGMAN[mistakes], (WIDTH // 2 - (HANGMAN[mistakes].get_width() // 2), 50))

        if len(guessing_word) > 7:
            temp_start = 0
            temp_width = WIDTH
        else:
            temp_start = (7 - len(guessing_word)) * 40
            temp_width = WIDTH - (7 - len(guessing_word)) * 40

        for index in range(len(guessing_word)):
            line_length = round((temp_width - temp_start - 20) // len(guessing_word)) - 20
            start_x = 20 + temp_start + index * round((temp_width - temp_start - 20) // len(guessing_word))
            end_x = start_x + line_length
            y = alphabet_buttons[0].y - 20 - LINE_WIDTH
            pygame.draw.line(win, MAIN_GAME_COLOR, [start_x, y], [end_x, y], LINE_WIDTH)
            if guessed[index] != '_':
                letter_font = pygame.font.SysFont(MAIN_FONT, MAIN_FONT_SIZE)
                letter = letter_font.render(guessed[index], 1, MAIN_GAME_COLOR)
                win.blit(letter, (start_x + line_length // 2 - letter.get_width() // 2, y - letter.get_height() - 2))

        for button in alphabet_buttons:
            if button.text not in guessed_letters:
                button.draw(win)
    else:
        play_button.draw(win)
        quit_button.draw(win)

    pygame.display.update()


def main():
    global playing
    global guessed
    global mistakes
    global guessed_letters

    # clock = pygame.time.Clock()
    pygame.init()
    window = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption('Hangman')

    running = True
    while running:
        # clock.tick(30)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if playing:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in alphabet_buttons:
                        if button.is_over(pos) and button.text not in guessed_letters:
                            if button.text in guessing_word:
                                print('you guessed a letter')
                                index = 0
                                for i in range(guessing_word.count(button.text)):
                                    letter_ind = guessing_word.find(button.text, index)
                                    guessed = guessed[:letter_ind] + button.text + guessed[letter_ind + 1:]
                                    index = letter_ind + 1
                            else:
                                mistakes += 1
                                print('No such letter')

                            guessed_letters.append(button.text)
                            if guessing_word == guessed:
                                end_game(window, True)
                            elif mistakes == 6:
                                end_game(window, False)

                if event.type == pygame.MOUSEMOTION:
                    for button in alphabet_buttons:
                        if button.is_over(pos) and button.text not in guessed_letters:
                            button.color = ALPHABET_EXTRA_COLOR
                        else:
                            button.color = BG_COLOR
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_over(pos):
                        playing = True
                        start_new_game()
                        draw_main_window(window)
                    elif quit_button.is_over(pos):
                        running = False
                        break

                if event.type == pygame.MOUSEMOTION:
                    if play_button.is_over(pos):
                        play_button.color = MENU_BUTTON_EXTRA_COLOR
                    elif quit_button.is_over(pos):
                        quit_button.color = MENU_BUTTON_EXTRA_COLOR
                    else:
                        play_button.color = MENU_BUTTON_COLOR
                        quit_button.color = MENU_BUTTON_COLOR

        draw_main_window(window)

    pygame.quit()


if __name__ == '__main__':
    main()
