from Data import Filter, Result
from collections import defaultdict
from random import choice

def get_I(w1, w2):
    for i in w1:
        if i in w2:
            return True
    return False

def get_B(M: dict[str, float]):
    B = []
    for w in M.keys():
        if B == [] or M[w] > M[B[0]]:
            B = [w]
        elif M[w] == M[B[0]]:
            B.append(w)
    return B

def get_S(L: list[str]):
    if len(L) <= 1:
        return L
    LN = [l for l in L[1:] if not get_I(L[0], l)]
    LN = get_S(LN)
    LN.append(L[0])
    return LN

def get_Mt(M, w1):
    return {w2: M[w2] for w2 in M.keys() if not get_I(w1, w2)}

def get_P(M):
    SBM = get_B(M)
    print(SBM)
    for w in SBM:
        SBM.extend(get_P(get_Mt(M, w)))
    return SBM

def best_seed_word(A, C, N):
    F = {}
    for letter in C:
        F[letter] = 0

    for w in A:
        for c1 in C:
            F[c1] += w.count(c1)

    for c1 in C:
        F[c1] /= sum([len(w) for w in A])

    W = [w for w in A if len(set(w)) == 5]

    if len(W) < N:
        W = A

    M = {w: sum([F[c] for c in w]) for w in W}
    I = sorted(M.keys(), key=lambda w: M[w], reverse=True)[:N]
    
    return I

class Solver:
    def __init__(self, valid_words: list[str]) -> None:
        self.valid_words = valid_words

    def best_guesses(self, filter: Filter, count: int) -> list[str]:
        words = filter.filter_words(self.valid_words)
        if len(words) == 0:
            return self.valid_words
        return best_seed_word(words, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", count)
    

def test_ai(words: str, answers: str, games: int):
    scores = []

    for _ in range(games):
        target = choice(answers)
        solver = Solver(words)
        filter = Filter([])
        for i in range(6):
            guess = solver.best_guesses(filter, 1)[0]
            if guess == target:
                scores.append(i+1)
                break
            if i == 5:
                #scores.append(i+2)
                break
            filter.results.append(Result.from_guess(guess, target))

    return scores

def load_data() -> tuple[list[str]]:
    # Read the valid guesses from the file
    with open("wordle-nyt-allowed-guesses.txt", "r") as f:
        valid_guesses = [word.strip().upper() for word in f]

    # Read the valid secret words from the file
    with open("wordle-nyt-answers-alphabetical.txt", "r") as f:
        valid_secret_words = [word.strip().upper() for word in f]

    # All valid secrets word can also be guessed (ofcourse)
    valid_guesses.extend(valid_secret_words)
    return valid_guesses, valid_secret_words


def main():
    valid_guesses, valid_secret_words = load_data()
    scores = test_ai(valid_guesses, valid_secret_words, 1000)
    print(sum(scores) / len(scores))

if __name__ == "__main__":
    main()
