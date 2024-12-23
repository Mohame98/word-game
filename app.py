from flask import Flask, render_template, request, session, flash, redirect
from letter_state import LetterState, WordState, group_attempts, get_random_word 
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()
valid_words = list(line.strip() for line in open("words.txt"))

@app.get("/")
def get_home():
    if 'game' not in session:
        word_to_guess = get_random_word(valid_words)
        session['game'] = {
            'word_to_guess': word_to_guess,
            'guessed_letters': [],
            'winner': False,
            'attempts': [],
            'colors': [],
            'row': 0,
        }

    game = session['game']
    return render_template("game.html", game=game)

@app.post("/playgame")
def play_game():
    if 'game' not in session:
        flash("No game session found. Start a new game.")
        return redirect("/")
    
    game = session['game']
    letter_state = LetterState(game['word_to_guess'])
    word = WordState(valid_words, game['word_to_guess'])

    for col in range(5):
        letter = request.form.get(f'letter_{game["row"]}_{col}')
        if not letter:
            flash("five letters Are Required!")
            return redirect("/")
          
        game['guessed_letters'].append(letter.lower())
    game['attempts'] = group_attempts(game['guessed_letters'])

    valid = word.is_valid_guess(game['attempts'])
    if not valid:
        game['attempts'].pop(-1)
        game['guessed_letters'] = game['guessed_letters'][:-5]
        flash("Please enter a valid word!")
        return redirect("/") 
        
    letter_state.color_change(game['attempts'], game['colors'])

    game['winner'] = word.is_winning_guess(game['attempts'])
    if game['winner']:
        session['message'] = "Congratulations! You won!"
        return redirect("/")
        
    if len(game['attempts']) == 6:
        session['message'] = "You are out of guesses!"
        return redirect("/")
        
    if len(game['attempts']) <= 6:
        game['row'] += 1

    session['game'] = game
    return redirect("/")

@app.post("/newgame")
def reset_game():
    session.pop('game')
    if 'message' in session:
        session.pop('message')
    return redirect("/")