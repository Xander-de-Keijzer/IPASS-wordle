class Result:
    def __init__(self, guess: str, yellows: list[int], greens: list[int]) -> None:
        self.guess = guess
        self.yellows = yellows
        self.greens = greens

        self.has_destructured = False
        self.gray = []
        self.green = []
        self.yellow = []

    def get_color(self, position: int) -> str:
        if position in self.greens:
            return "green"
        if position in self.yellows:
            return "yellow"
        return "gray"
    
    def get_colors(self) -> list[str]:
        return [self.get_color(index) for index in range(len(self.guess))]
            
    def get_yellows(self) -> list[str]:
        if self.has_destructured:
            return self.yellow
        return [
            letter 
            for index, letter 
            in enumerate(self.guess) 
            if index in self.yellows
        ]
    
    def get_greens(self) -> list[str]:
        if self.has_destructured:
            return self.green
        return [
            letter 
            for index, letter 
            in enumerate(self.guess) 
            if index in self.greens
        ]
    
    def get_grays(self) -> list[str]:
        if self.has_destructured:
            return self.gray
        return [
            letter 
            for letter 
            in self.guess
            if letter not in self.get_yellows() and letter not in self.get_greens()
        ]
    
    def filter(self, word: str) -> bool:
        for letter in self.get_grays(): # Return false if word contains any gray letters
            if letter in word:
                return False
            
        for letter in self.get_greens(): # Return false if word doesn't contain all green letters
            if letter not in word:
                return False
            
        for index, letter in enumerate(word): # Return false if word has the same letter on a yellow
            if index in self.yellows and self.guess[index] == letter:
                return False
            
        for letter in self.get_yellows(): # Return false if word doesn't contain all yellow letters
            if letter not in word:
                return False
            
        return True

    def from_guess(guess: str, answer: str):
        result = Result(guess, [], [])
        for index, letter in enumerate(guess):
            if letter == answer[index]:
                result.greens.append(index)
                result.green.append(letter)

        for index, letter in enumerate(guess):
            if index in result.greens:
                continue
            if letter in answer and answer.count(letter) - result.get_greens().count(letter) - result.get_yellows().count(letter) > 0:
                result.yellows.append(index)
                result.yellow.append(letter)

        for index, letter in enumerate(guess):
            if index not in result.greens and index not in result.yellows:
                result.gray.append(letter)

        result.has_destructured = True
        return result
    
    def __repr__(self) -> str:
        return f"Result({self.guess=}, {self.greens=}, {self.yellows=})"

    
class Filter:
    def __init__(self, results: list[Result]) -> None:
        self.results = results

    def filter_word(self, word: str) -> bool:
        for result in self.results:
            if not result.filter(word):
                return False
        return True

    def filter_words(self, words: list[str]) -> list[str]:
        return [word for word in words if self.filter_word(word)]
    
    def filter_scores(self, words: dict[str, float]) -> dict[str, float]:
        return {word: score for word, score in words.items() if self.filter_word(word)}
    
    def __repr__(self) -> str:
        return f"Filter(results={self.results})"
    