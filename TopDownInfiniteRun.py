import curses
import random

#In questa area iniziale ci sono le classi utilizzate per creare il gioco

# Classe che contiene le informazioni dello stato del gioco
class GameState:

    def __init__(self, turns_to_play, spawn_chance, change_scoring_symbol_chance, player_score=0, scoring_symbol=''):
        self.player_score = player_score
        self.scoring_symbol = scoring_sybol

        self.remaining_turns = turns_to_play
        self.spawn_chance = spawn_chance
        self.change_scoring_symbol_chance = change_scoring_symbol_chance

        self.all_symbols = ['+', '-', '*', '/', '=']

    def set_scoring_symbol(self, scoring_symbol):
        self.scoring_symbol = scoring_symbol

    def get_scoring_symbol(self):
        return self.scoring_symbol

    def get_all_symbols(self):
        return self.all_symbols

    def update_player_score(self, score):
        self.player_score += score
        return self.player_score

    def get_player_score(self):
        return self.player_score

    def reset_player_score(self):
        self.player_score = 0
        return self.player_score

    def get_remianing_turns(self):
        return self.remaining_turns

    def turn_end(self):
        self.remaining_turns -= 1
        if self.remaining_turns == 0:
            print("Game Over!")
            return False  # Se viene ritornato falso il gioco è finito e viene mostrato il punteggio finale
        # Se il gioco non è finito aggiorna il simbolo vincente
        if random.random() < self.change_scoring_symbol_chance:
            self.set_scoring_symbol(self.get_random_symbol())
        return True

    def change_spawn_chance(self, variation):
        self.spawn_chance += variation

    def is_symbol_spawning(self):
        return random.random() < self.spawn_chance

    def get_random_symbol(self):
        return random.choice(self.all_symbols)


# Classe che contiene le informazioni dell'ara di gioco
class GameArea:

    def __init__(self, width, height, has_border=True):
        self.width = width
        self.height = height
        self.has_border = has_border

        self.window = None

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_has_border(self):
        return self.has_border

    def print_game_area(self):
        # Set up the screen
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(100)
        
        self.window = curses.newwin(self.height, self.width, 0, 0)

        if self.has_border:
            self.window.border(0)

        return self.window

    def clear_game_area(self):
        self.window.clear()
        if self.has_border:
            self.window.border(0)

    def generate_points(start, end, num_points):
        if num_points > (end - start + 1):
            return []
        else:
            step = (end - start) / (num_points - 1)
            return [round(start + step * i) for i in range(num_points)]

    def get_spawn_positions(self, number_of_spawn_positions):
        spawning_points_max = width - 2
        if number_of_spawn_positions > spawning_points_max:
            print("Sono stati richiesti troppi punti di spawn! puoi chiederne al massimo " + spawning_points_max)
            return []
        else:
            return generate_points(1, width - 1, number_of_spawn_positions)

    def is_end_position(self, position):
        return position == height

    def print_actor(self, actor):
        self.window.addstr(actor.x_pos, actor.y_pos, actor.symbol)      

    def print_score(self, score):
        self.window.addstr(1, self.width-10, 'Score: ' + str(score))

    def print_turns(self, turns):
        self.window.addstr(1, self.width-4, 'Turns: ' + str(score))

    def print_end_score(self, score):
        self.clear_game_area()
        self.window.addstr(5, self.width-6, 'Final Score: ' + str(score))

# Classe che contine le informazioni riguardo il player
class Player:

    def __init__(self, symbol, game_area):
        self.symbol = symbol
        self.game_area = game_area

        self.x_pos = game_area.get_width() // 2
        self.y_pos = game_area.get_height() - 2

    def move_x(self, movement):
        self.x_pos += movement
        self.x_pos = max(1, min(self.x_pos, game_area.get_width() - 1))


# Classe che contine l'informazione dei simboli da raccogliere
class CollectableItem:

    def __init__(self, symbol, score=0, x_pos=0, y_pos=0, visible=True):
        self.symbol = symbol
        self.score = score

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.visible = visible

    def get_symbol(self):
        if(self.is_visible):
            return self.symbol
        else:
            return ' '

    def get_score(self):
        return self.score

    def set_score(self, new_score):
        self.score = new_score

    def get_position(self):
        return self.position
        
    def is_visible(self):
        return self.visible

    def set_visible(self, visible):
        self.visible = visible

    def move_one_step_down(self):
        self.y_pos += 1

# Qui è dove inizia il vero e proprio gioco

def main(stdscr):

    # Questa è la parte iniziale, viene eseguito tutto una volta sola prima che inizi la partita

    # Si crea l'area di gioco
    game_area = GameArea(10, 12) # non devo indicare anche True dato che si tratta del valore di default
    window = game_area.print_game_area()
    
    # Set up del player, gli viene dato un simbolo, e viene posizionato a due unità dal fondo e al centro dell'area di gioco.
    player = Player('^', game_area.get_width(), game_area.get_height() - 2)
    
    # Viene creato il game state dove conterremo le informazioni sulla progressione di gioco. 
    # Impostiamo 50 turni, una probabilità ogni turno di spawnare un nuovo dimbolo del 50% e una probabilità del 20% di cambiare il simbolo vincente
    game_state = GameState(50, 0.5, 0.2)

    # Set up the spawning positions
    object_positions = game_area.get_spawn_positions(5)

    # list of current exiting objects
    current_objects = []

    # Questo è il loop di gioco. Viene eseguito costantemente fino a fine esecuzione
    while True:

        # Stampa a schermo di tutte le informazioni

        # Refresh the game window
        game_area.clear_game_area()
        # stampa a schermo il player
        game_area.print_actor(player)
        #stampa tutti gli altri oggetti
        for i in range(len(current_objects)):
            game_area.print_actor(current_objects[i])
        game_area.print_score(game_state.get_player_score())
        game_area.print_turns(game_state.get_remianing_turns())

        # Lettura degli input del giocatore

        # Get the user input. Questa è la parte da cambiare con microbit
        key = w.getch()

        # Quit the game
        if key == ord('q'):
            break

        # Move the player
        if key == ord('a'):
            player.move_x(-1)
        elif key == ord('d'):
            player.move_x(1)

        # Move the objects down
        for i in range(len(current_objects)):
            current_objects[i].move_one_step_down()

        # Check for collision with the player
        for i in range(len(current_objects)):
            if current_objects[i].x_pos == player.x_pos and current_objects[i].y_pos == player.y_pos:
                score += current_objects[i].get_score()
                current_objects[i].set_visible(False)

        # Check if the objects have reached the end
        for i in range(len(current_objects)):
            if game_area.is_end_position(current_objects[i].y_pos):
                current_objects[i].set_visible(False)

        # Remove refereces to invisible objects
        current_objects = [item for item in current_objects if item.is_visible()]

        # Check if the game is over
        if not game_state.turn_end():
            game_area.print_end_score(game_state.get_player_score())
            sleep(5000)
            break

        # Check if a new symbol should be generated
        if game_state.is_symbol_spawning():
            current_objects.add(CollectableItem(game_state.get_random_symbol()))

        # Aggiorna il punteggio di tutti i simboli
        for i in range(len(current_objects)):
            if current_objects[i].get_symbol() == game_state.get_scoring_symbol():
                current_objects[i].set_score(10)
            else:
                current_objects[i].set_score(0)



if __name__ == '__main__':
    curses.wrapper(main)