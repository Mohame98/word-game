import random


class LetterState:
    def __init__(self, word_to_guess):
        self.word_to_guess = word_to_guess

    def color_change(self, attempts, colors):
        colors_array = [] 
        used_letters = []
        most_recent_attempt = attempts[-1]
        
        for i in range(5):
            if most_recent_attempt[i] == self.word_to_guess[i]:
                used_letters.append(most_recent_attempt[i]) 
                colors_array.append('green')
            else:
                colors_array.append(None)  
        
        for i in range(5):
            if colors_array[i] == 'green':
                continue 
            if most_recent_attempt[i] in self.word_to_guess:
                letter_count_in_word = self.word_to_guess.count(most_recent_attempt[i])
                letter_count_in_guess = most_recent_attempt[:i].count(most_recent_attempt[i]) 
                + used_letters.count(most_recent_attempt[i])

                if letter_count_in_guess < letter_count_in_word:
                    colors_array[i] = 'yellow'
                    used_letters.append(most_recent_attempt[i])
                else:
                    colors_array[i] = 'gray'
            else:
                colors_array[i] = 'gray'
        colors.append(colors_array)
        return colors


class WordState:  
    def __init__(self, valid_words, word_to_guess):
        self.valid_words = valid_words
        self.word_to_guess = word_to_guess

    def is_valid_guess(self, attempts):
        most_recent_attempt = attempts[-1]
        most_recent_word = ''.join(most_recent_attempt).lower()
        for word in self.valid_words:
            if len(most_recent_word) == 5 and word == most_recent_word:
                return True
        return False
    
    def is_winning_guess(self, attempts):   
        most_recent_attempt = attempts[-1]
        most_recent_word = ''.join(most_recent_attempt).lower()
        if most_recent_word == self.word_to_guess:
                return True
        return False
    

def group_attempts(letters):
    attempts = []
    for i in range(0, len(letters), 5):
        attempts.append(letters[i:i+5])
    return attempts

def get_random_word(valid_words):
    return random.choice(valid_words).lower()