import unittest
import bot
from bot import CharacterRegistry, GPTCharacter, Conversation, DatabaseManager
from unittest.mock import MagicMock, patch
import psycopg2
from dotenv import load_dotenv
import os

def load_test_environment_variables():
    load_dotenv('test.env')

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

class TestConversation(unittest.TestCase):
    def setUp(self):
        # Initialize the CharacterRegistry and the Conversation for testing
        self.character_registry = CharacterRegistry()
        self.conversation = Conversation(self.character_registry)

    def test_add_message(self):
        # Test adding messages to the conversation
        self.conversation.add_message('user', 'Hello, how are you?')
        self.conversation.add_message('assistant', 'I am doing well, thank you!')
        self.assertEqual(len(self.conversation.messages), 2)

    def test_add_character(self):
        # Test adding characters to the conversation
        self.conversation.add_character('Боба')
        self.conversation.add_character('Зюзя')
        self.assertEqual(len(self.conversation.get_character_names()), 2)

    def test_generate_response(self):
        # Test generating responses for characters in the conversation
        self.conversation.add_character('Jack')
        response = self.conversation.generate_response('Jack')
        self.assertIsInstance(response, str)

    def test_reduce_context_size(self):
        # Test reducing the context size of the conversation
        self.conversation.add_character('Боба')
        self.conversation.add_message('user', 'How are you doing?')
        self.conversation.reduce_context_size('Боба')
        self.assertEqual(len(self.conversation.messages), 2)

    def test_get_messages(self):
        # Test getting the list of messages in the conversation
        self.conversation.add_message('user', 'Hello, how are you?')
        self.conversation.add_message('assistant', 'I am doing well, thank you!')
        messages = self.conversation.get_messages()
        self.assertEqual(len(messages), 2)

    def test_get_character_names(self):
        # Test getting the names of all characters in the conversation
        self.conversation.add_character('Боба')
        self.conversation.add_character('Зюзя')
        character_names = self.conversation.get_character_names()
        self.assertEqual(len(character_names), 2)
        self.assertIn('Боба', character_names)
        self.assertIn('Зюзя', character_names)

class TestDatabaseManagerConnecttion(unittest.TestCase):
    def setUp(self):
        # Set up test database connection
        load_test_environment_variables()
        self.dbname=os.environ.get('TEST_DATABASE_NAME')
        self.user=os.environ.get('TEST_DATABaSE_USER_NAME')
        self.password=os.environ.get('TEST_DATABSAE_PASSWORD')
        self.host=os.environ.get('TEST_DATABASE_HOST')
        self.port=os.environ.get('TEST_DATABASE_PORT')
    @patch('bot.psycopg2.connect')
    def test_connect_successful(self, mock_connect):
        # Arrange
        db_manager = DatabaseManager(self.dbname, self.user, self.password, self.host, self.port)

        # Act
        connection = db_manager.connection

        # Assert
        self.assertIsNotNone(connection)
        print(connection)
        mock_connect.assert_called_once()

    @patch('bot.psycopg2.connect', side_effect=bot.psycopg2.Error)
    def test_connect_unsuccessful(self, mock_connect):
        with self.assertRaises(RuntimeError):
            db_manager = DatabaseManager(self.dbname, self.user, self.password, self.host, self.port)

class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up test database connection
        load_test_environment_variables()
        dbname=os.environ.get('TEST_DATABASE_NAME')
        user=os.environ.get('TEST_DATABaSE_USER_NAME')
        password=os.environ.get('TEST_DATABSAE_PASSWORD')
        host=os.environ.get('TEST_DATABASE_HOST')
        port=os.environ.get('TEST_DATABASE_PORT')

        cls.db_manager = DatabaseManager(dbname, user, password, host, port)

    def tearDown(self):
        self.clean_up_test_data()  # Roll back any changes made during the test

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database after all tests
        cls.db_manager.connection.close()
    def clean_up_test_data(self):
        cursor = self.db_manager.connection.cursor()

        # Delete all data that were inserted during setup
        cursor.execute("DELETE FROM messages;")
        cursor.execute("DELETE FROM characters;")
        cursor.execute("DELETE FROM conversations;")

        # Commit the deletion and close the cursor
        self.db_manager.connection.commit()
        cursor.close()

    def test_insert_message(self):
        conversation_id = 1
        role = "user"
        content = "Hello, world!"

        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id) VALUES (%s);",
            (conversation_id, )
        )
        # Call the function you want to test
        self.db_manager.insert_message(conversation_id, role, content)

        # Fetch the inserted data from the test database and assert its correctness
        self.db_manager.cursor.execute("SELECT conversation_id, role, content FROM messages;")
        result = self.db_manager.cursor.fetchall()

        self.assertEqual(len(result), 1, "One row should have been inserted")
        self.assertEqual(result[0], (conversation_id, role, content))

    def test_insert_message_multiple_calls(self):
        # Arrange
        conversation_id = 1
        role = "user"
        content = "Hello, world!"

        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id) VALUES (%s);",
            (conversation_id, )
        )

        for i in range(5):
            self.db_manager.insert_message(conversation_id, role, content)
        self.db_manager.cursor.execute("SELECT * FROM messages WHERE conversation_id = %s;", (conversation_id,))
        messages = self.db_manager.cursor.fetchall()
        self.assertEqual(len(messages), 5)

    def test_delete_all_messages(self):
        # Arrange
        conversation_id = 1
        role = "user"
        content = "Hello, world!"

        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id) VALUES (%s);",
            (conversation_id, )
        )
        self.db_manager.cursor.execute("SELECT * FROM messages WHERE conversation_id = %s;", (conversation_id,))
        messages = self.db_manager.cursor.fetchall()

        for i in range(5):
            self.db_manager.insert_message(conversation_id, role, content)

        # Act
        self.db_manager.delete_all_messages(conversation_id)
        self.db_manager.connection.commit()  

        # Assert
        self.db_manager.cursor.execute("SELECT * FROM messages WHERE conversation_id = %s;", (conversation_id,))
        messages = self.db_manager.cursor.fetchall()

        self.assertEqual(len(messages), 0)  # Assert that all messages for the conversation are deleted

    def test_insert_characters(self):
        # Arrange
        conversation_id = 1
        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id) VALUES (%s);",
            (conversation_id, )
        )
        names = ["Alice", "Bob", "Charlie"]  # Replace with character names to insert
        self.db_manager.cursor.execute(
                    "INSERT INTO characters (name, conversation_id) VALUES (%s, %s);",
                    ('Alice', conversation_id)
                )

        # Act  # Replace with existing character names in the database
        self.db_manager.insert_characters(conversation_id, names)

        # Assert
        cursor = self.db_manager.cursor
        cursor.execute("SELECT name FROM characters WHERE conversation_id = %s;", (conversation_id,))
        inserted_names = [row[0] for row in cursor.fetchall()]

        expected_names = ["Alice", "Bob", "Charlie"]  # Expected inserted names
        self.assertEqual(inserted_names, expected_names)

    def test_get_character_names(self):
        # Arrange
        conversation_id = 1
        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id) VALUES (%s);",
            (conversation_id, )
        )
        expected_names = ["Alice", "Bob", "Charlie"]  # Replace with expected character names
        # Pre-write names into the database
        for character_name in expected_names:
            self.db_manager.cursor.execute(
                "INSERT INTO characters (name, conversation_id) VALUES (%s, %s);",
                (character_name, conversation_id)
            )
        # Act
        character_names = self.db_manager.get_character_names(conversation_id)

        # Assert
        self.assertEqual(character_names, expected_names)
    def test_save_conversation(self):
        # Arrange
        conversation_id = 1
        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id) VALUES (%s);",
            (conversation_id, )
        )
        conversation = Conversation(CharacterRegistry())
        for i in range(5):
            conversation.add_user_message('Hello, World!', 'John')
        conversation.add_character('Jack')
        conversation.token_handler.set_tokens(1000)

        # Act
        self.db_manager.save_conversation(conversation_id, conversation)

        # Assert
        # Check conversations table
        cursor = self.db_manager.connection.cursor()
        cursor.execute("SELECT tokens FROM conversations WHERE id = %s;", (conversation_id,))
        tokens = cursor.fetchone()[0] 
        expected_tokens = 1000  # Replace with expected tokens
        self.assertEqual(tokens, expected_tokens)

        # Check characters table
        cursor.execute("SELECT name FROM characters WHERE conversation_id = %s;", (conversation_id,))
        character_names = [row[0] for row in cursor.fetchall()]
        expected_character_names = ['Jack']  # Replace with expected character names
        self.assertEqual(character_names, expected_character_names)

        # Check messages table
        cursor.execute("SELECT role, content FROM messages WHERE conversation_id = %s;", (conversation_id,))
        messages = cursor.fetchall()
        self.assertEqual(len(messages), 7)

    def test_get_messages(self):
        # Arrange
        conversation_id = 1  # Replace with a valid conversation ID
        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id) VALUES (%s);",
            (conversation_id, )
        )
        expected_messages = [
            ('user', 'Hello'),
            ('user', 'Hi'),
            ('user', 'Hey!')
        ] 
        for message in expected_messages:
            user = message[0]
            content = message[1]
            self.db_manager.insert_message(conversation_id, user, content)
        
        # Act
        actual_messages = self.db_manager.get_messages(conversation_id)

        # Assert
        self.assertEqual(actual_messages, expected_messages)
    def test_get_tokens(self):
        # Arrange
        conversation_id = 1 
        expected_tokens = 1000
        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id, tokens) VALUES (%s, %s) ",
            (conversation_id, expected_tokens)
        )
        
        # Act
        actual_tokens = self.db_manager.get_tokens(conversation_id)

        # Assert
        self.assertEqual(actual_tokens, expected_tokens)
    def test_is_conversation_in_database(self):
        # Arrange
        conversation_id = 1 
        expected_tokens = 1000
        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id, tokens) VALUES (%s, %s) ",
            (conversation_id, expected_tokens)
        )
        
        # Act
        actual_flag1 = self.db_manager.is_conversation_in_database(conversation_id)
        # Chack a non existing conversation
        actual_flag2 = self.db_manager.is_conversation_in_database(123)

        # Assert
        self.assertEqual(actual_flag1, True)
        self.assertEqual(actual_flag2, False)
    
    def test_read_conversation(self):
        # Arrange
        conversation_id = 1 
        expected_tokens = 1000
        self.db_manager.cursor.execute(
            "INSERT INTO conversations (id, tokens) VALUES (%s, %s) ",
            (conversation_id, expected_tokens)
        )
        
        self.db_manager.insert_message(conversation_id, 'user', 'Hey!')
        self.db_manager.insert_message(conversation_id, 'user', 'Hello!')
        expected_messages = [{'role': 'user', 'content': 'Hey!'},
                             {'role': 'user', 'content': 'Hello!'}]
        expected_names = ["Alice", "Bob", "Charlie"]  # Replace with expected character names
        # Pre-write names into the database
        for character_name in expected_names:
            self.db_manager.cursor.execute(
                "INSERT INTO characters (name, conversation_id) VALUES (%s, %s);",
                (character_name, conversation_id)
            )
        expected_output = (expected_tokens, expected_names, expected_messages)
        # Act
        actual_output = self.db_manager.read_conversation(conversation_id)

        # Assert
        self.assertEqual(actual_output, expected_output)
    def test_read_conversation_non_existent(self):
        # Arrange
        expected_output = None
        # Act
        actual_output = self.db_manager.read_conversation(123)

        # Assert
        self.assertEqual(actual_output, expected_output)