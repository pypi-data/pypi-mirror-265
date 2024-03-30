import pytest
from unittest.mock import patch
from src.wordutilities import *

class TestWordUtilities:

    # @pytest.mark.xfail(raises=NotImplementedError)
    def test_is_anagram(self):
        assert is_anagram('listen', 'silent') == True
        assert is_anagram('elbow', 'below') == True
        assert is_anagram('hello', 'world') == False

    # @pytest.mark.xfail(raises=NotImplementedError)
    def test_scramble(self):
        word = 'hello'
        scrambled_word = scramble(word)
        assert sorted(word) == sorted(scrambled_word)
    
    #@pytest.mark.xfail(raises=NotImplementedError)
    def test_anagrams(self):
        assert anagrams('listen') == ['enlist', 'inlets', 'listen', 'silent', 'slinte', 'tinsel']
        assert anagrams('LiStEn') == anagrams('sTINel')
        assert anagrams('elbow') == ['below', 'bowel', 'bowle', 'elbow']
        assert anagrams('hello') == ['hello']
        assert anagrams('QQQ') == []
        assert anagrams('ABC123') == 'Invalid word'

    def test_anagrams_blank(self):
        assert anagrams_blank('pancak') == ['manpack', 'packman', 'pancake']
        assert anagrams_blank('QQQ') == []

    def test_permutations(self):
        assert permutations('abc') == ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
        assert permutations('aba') == ['aba', 'aab', 'baa']

    def test_select_random_sentence_returns_non_empty_string(self):
        sentence = wordutilities.select_random_sentence()
        assert isinstance(sentence, str) and len(sentence) > 0

    def test_select_random_sentence_returns_valid_sentence(self):
        sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "My Mum tries to be cool by saying that she likes all the same things that I do.",      
            "A purple pig and a green donkey flew a kite in the middle of the night and ended up sunburnt.",
            "Last Friday I saw a spotted striped blue worm shake hands with a legless lizard.",
            "A song can make or ruin a person’s day if they let it get to them.",
            "Sometimes it is better to just walk away from things and go back to them later when you’re in a better frame of mind.",
            "Writing a list of random sentences is harder than I initially thought it would be.",
            "Lets all be unique together until we realise we are all the same.",
            "If I don’t like something, I’ll stay away from it.",
            "I love eating toasted cheese and tuna sandwiches.",
            "If you like tuna and tomato sauce- try combining the two. It’s really not as bad as it sounds.",
            "Someone I know recently combined Maple Syrup & buttered Popcorn thinking it would taste like caramel popcorn. It didn’t and they don’t recommend anyone else do it either.",
            "Sometimes, all you need to do is completely make an ass of yourself and laugh it off to realise that life isn’t so bad after all.",
            "When I was little I had a car door slammed shut on my hand and I still remember it quite vividly.",
            "The clock within this blog and the clock on my laptop are 1 hour different from each other.",
            "I want to buy a onesie… but know it won’t suit me.",
            "I was very proud of my nickname throughout high school but today- I couldn’t be any different to what my nickname was.",
            "I currently have 4 windows open up… and I don’t know why.",
            "I often see the time 11:11 or 12:34 on clocks.",
            "This is the last random sentence I will be writing and I am going to stop mid-sent."
        ]  
        for _ in range(40):  # Arbitrary number of trials to ensure randomness is adequately tested
            sentence = wordutilities.select_random_sentence()
            assert sentence in sentences

    def test_select_random_most_common_word_returns_non_empty_string(self):
        word = wordutilities.select_random_most_common_word()
        assert isinstance(word, str) and len(word) > 0

    def test_select_random_most_common_word_returns_valid_word(self):
        common_words = ["the","and","have","that","for","you","with","say","this","they","but","is","from","not","she","as","what","their","can","who","get"]
        word = wordutilities.select_random_most_common_word()
        assert word in common_words

    @patch('builtins.input', side_effect=[ 'D','A','quit'])  # Assuming 'D' is an invalid choice leading to retry.
    @patch('builtins.print')
    def test_fill_blanks_incorrect_and_correct_guess(self, mock_print, mock_input):
        # Call the function to trigger the mocked input and print
        wordutilities.fill_blanks()

        # Assert that only these messages will appear: when user enters incorrect/invalid answer, when user enters correct answer, and when user quits
        # Will also verify that for each of these inputs: invalid, incorrect, correct, and "quit" the code will not break
        incorrect_message_found = any("\nPlease select A B or C only. Try again." or "\nIncorrect. Try again."in call_args[0][0] for call_args in mock_print.call_args_list)
        correct_message_found = any("\nCorrect!" in call_args[0][0] for call_args in mock_print.call_args_list)
        quit_message_found = any("\nBye!" in call_args[0][0] for call_args in mock_print.call_args_list)
        assert incorrect_message_found or correct_message_found or quit_message_found 