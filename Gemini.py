import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyCc6ifOk7iTMgKZR6JsACRi9sja7jFzdb4")

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Here's a Python function that checks whether a word is a palindrome.\nAdd 10 different unit tests for this snippet with comments. Follow up with a short explanation of what was done.\n\n\n```\ndef is_palindrome(word):\n  \"\"\"\n  Checks whether a word is a palindrome.\n\n  Args:\n    word: The word to check.\n\n  Returns:\n    True if the word is a palindrome, False otherwise.\n  \"\"\"\n\n  # Convert the word to lowercase and remove non-alphanumeric characters.\n  word = ''.join(char.lower() for char in word if char.isalnum())\n\n  # Check if the word is the same forwards and backwards.\n  return word == word[::-1]\n```",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```python\nimport unittest\n\ndef is_palindrome(word):\n  \"\"\"\n  Checks whether a word is a palindrome.\n\n  Args:\n    word: The word to check.\n\n  Returns:\n    True if the word is a palindrome, False otherwise.\n  \"\"\"\n\n  # Convert the word to lowercase and remove non-alphanumeric characters.\n  word = ''.join(char.lower() for char in word if char.isalnum())\n\n  # Check if the word is the same forwards and backwards.\n  return word == word[::-1]\n\nclass TestIsPalindrome(unittest.TestCase):\n\n  def test_empty_string(self):  #Test with an empty string\n    self.assertTrue(is_palindrome(\"\"))\n\n  def test_single_character(self):  # Test with a single character\n    self.assertTrue(is_palindrome(\"a\"))\n\n  def test_simple_palindrome(self):  # Test with a simple palindrome\n    self.assertTrue(is_palindrome(\"madam\"))\n\n  def test_palindrome_with_spaces(self):  #Test with spaces\n    self.assertTrue(is_palindrome(\"Race car\"))\n\n  def test_palindrome_with_punctuation(self):  #Test with punctuation\n    self.assertTrue(is_palindrome(\"A man, a plan, a canal: Panama\"))\n\n  def test_not_palindrome(self):  # Test with a non-palindrome word\n    self.assertFalse(is_palindrome(\"hello\"))\n\n  def test_case_insensitive(self):  # Test case-insensitivity\n    self.assertTrue(is_palindrome(\"Madam\"))\n\n  def test_numbers_included(self):  #Test with numbers\n      self.assertTrue(is_palindrome(\"12321\"))\n\n  def test_mixed_case_and_punctuation(self): #Test mixed case and punctuation\n      self.assertTrue(is_palindrome(\"Was it a car or a cat I saw?\"))\n\n  def test_non_alphanumeric_characters(self): #Test with non-alphanumeric characters that should be ignored\n      self.assertFalse(is_palindrome(\"~!@#$%^\"))\n\n\nif __name__ == '__main__':\n  unittest.main()\n```\n\n**Explanation:**\n\nThe solution provides a `TestIsPalindrome` class that inherits from `unittest.TestCase`.  Inside this class, ten different test methods are defined, each testing a specific aspect of the `is_palindrome` function:\n\n1. **Empty String:** Checks if an empty string is considered a palindrome.\n2. **Single Character:** Checks if a single character string is a palindrome.\n3. **Simple Palindrome:** Checks a straightforward palindrome.\n4. **Palindrome with Spaces:** Checks a palindrome containing spaces.\n5. **Palindrome with Punctuation:** Checks a palindrome with punctuation marks.\n6. **Not Palindrome:** Checks a word that is not a palindrome.\n7. **Case Insensitive:** Verifies that the function is case-insensitive.\n8. **Numbers Included:** Checks a palindrome containing numbers.\n9. **Mixed Case and Punctuation:** Tests a more complex scenario with mixed case and punctuation.\n10. **Non-alphanumeric Characters:** Tests with only non-alphanumeric characters to ensure they are handled correctly.\n\nEach test method uses assertion methods from `unittest` (e.g., `self.assertTrue`, `self.assertFalse`) to check the expected output of the `is_palindrome` function.  The `if __name__ == '__main__':` block ensures that the tests are run only when the script is executed directly (not when imported as a module).  Running this script will execute all ten tests and provide a summary of the results in the console.\n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)