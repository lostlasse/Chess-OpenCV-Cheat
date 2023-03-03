from stockfish import Stockfish
import json

# reads config.json file
config_file = open("config.json")
config = json.load(config_file)
stockfish_path = config["stockfish_path"]
config_file.close()

def letter_to_xpos(letter): # convert letter to x position on the map
    letter = letter.lower()
    if letter == 'a':
        return 0
    if letter == 'b':
        return 1
    if letter == 'c':
        return 2
    if letter == 'd':
        return 3
    if letter == 'e':
        return 4
    if letter == 'f':
        return 5
    if letter == 'g':
        return 6
    if letter == 'h':
        return 7

    raise ValueError("Invalid letter.")

def pieces_to_map(input_map, input_pieces, color): # adds the input peaces to the input map
    for key, items in input_pieces.items():
        for coords in items:
            letter = coords[0:1]
            xpos = letter_to_xpos(letter)
            ypos = 8 - int(coords[1:2])

            code = ''

            if key == 'Pawns':
                code = 'P'
            elif key == 'Queen':
                code = 'Q'
            elif key == 'King':
                code = 'K'
            elif key == 'Knights':
                code = 'N'
            elif key == 'Bishops':
                code = 'B'
            elif key == 'Rooks':
                code = 'R'
            else:
                raise Exception(f'Undefined Input Pieces Key: {key}')
            
            if color == 'black':
                code = code.lower()
            
            input_map[ypos][xpos] = code

            # print(f'adding \'{key}\' ({code}) item ({coords}) -> ({ypos}|{xpos})')
    
    return input_map

def get_fen(bottom_pieces, top_pieces): # creates a fen string for the game layout
    chesspieces = [[0 for x in range(8)] for y in range(8)]

    chesspieces = pieces_to_map(chesspieces, bottom_pieces, 'white')
    chesspieces = pieces_to_map(chesspieces, top_pieces, 'black')

    fen = ''

    for ylist in chesspieces:
        counter = 0
        for i in ylist:
            if i == 0:
                counter = counter + 1
            elif counter >= 1 and not i == 0:
                fen = fen + str(counter)

                counter = 0
                fen = fen + i

            else:
                fen = fen + i

        if counter >= 1:
            fen = fen + str(counter)

        fen = fen + '/'

    fen = fen[0:(len(fen) - 1)] + ' w - - 0 1'

    return fen

def get_best_move(bottom_pieces, top_pieces): # calculates the best move

    stockfish = Stockfish(path=stockfish_path)

    fen_string = get_fen(bottom_pieces, top_pieces)

    stockfish.set_fen_position(fen_string)

    move = stockfish.get_best_move(2000)

    move = move.upper()

    split_strings = []
    n  = 2
    for index in range(0, len(move), n):

        split_strings.append(move[index : index + n])

    stockfish = None

    return split_strings[0], split_strings[1]
