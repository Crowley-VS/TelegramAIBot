import unittest
from bot import CharacterRegistry, GPTCharacter

class TestCharacterRegistry(unittest.TestCase):
    def setUp(self):
        # Create an instance of the CharacterRegistry class
        self.character_registry = CharacterRegistry()

    def test_load_characters(self):
        # Test if the characters are loaded correctly from the JSON file
        self.assertEqual(len(self.character_registry.characters), 3)

        # Test the data of the first character
        character1 = self.character_registry.get_character("Боба")
        self.assertIsInstance(character1, GPTCharacter)
        self.assertEqual(character1.name, "Боба")
        self.assertEqual(character1.description, "Добрый человек. Всегда выслушает и поддержит. Любит Genshin Impact. Ты говоришь по-русски. Вы отвечаете в стиле телефонных текстовых сообщений. Они довольно короткие.")

        # Test the data of the second character
        character2 = self.character_registry.get_character("Зюзя")
        self.assertIsInstance(character2, GPTCharacter)
        self.assertEqual(character2.name, "Зюзя")
        self.assertEqual(character2.description, "Ироничная девушка. Ты любишь грубоватые шутки. Ты говоришь по-русски. Вы отвечаете в стиле телефонных текстовых сообщений. Они довольно короткие.")

        # Test the data of the third character
        character3 = self.character_registry.get_character("Jack")
        self.assertIsInstance(character3, GPTCharacter)
        self.assertEqual(character3.name, "Jack")
        self.assertEqual(character3.description, "You are a kind person who is always there to listen. You speak English. You reply in short text message format. They are short.")

    def test_get_character(self):
        # Test getting characters by name
        character1 = self.character_registry.get_character("Боба")
        self.assertIsInstance(character1, GPTCharacter)
        self.assertEqual(character1.name, "Боба")

        character2 = self.character_registry.get_character("Зюзя")
        self.assertIsInstance(character2, GPTCharacter)
        self.assertEqual(character2.name, "Зюзя")

        character3 = self.character_registry.get_character("Jack")
        self.assertIsInstance(character3, GPTCharacter)
        self.assertEqual(character3.name, "Jack")

        # Test getting a character that does not exist
        non_existent_character = self.character_registry.get_character("NonExistent")
        self.assertIsNone(non_existent_character)