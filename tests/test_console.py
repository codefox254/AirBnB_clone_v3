#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import console
import inspect
import pep8
import unittest
HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")

    def test_HBNBCommand_method_docstrings(self):
        """Test for the presence of docstrings in HBNBCommand methods"""
        for name, method in inspect.getmembers(HBNBCommand, inspect.isfunction):
            self.assertIsNot(method.__doc__, None,
                             f"{name} method needs a docstring")
            self.assertTrue(len(method.__doc__) >= 1,
                            f"{name} method needs a docstring")

    def test_imports_in_console(self):
        """Test that all necessary imports are present in console.py"""
        with open('console.py', 'r') as file:
            console_contents = file.read()
        self.assertIn('import cmd', console_contents, "Missing import: cmd")
        self.assertIn('import sys', console_contents, "Missing import: sys")
        self.assertIn('import json', console_contents, "Missing import: json")
        self.assertIn('from models import storage', console_contents, "Missing import: storage")

    def test_help_command(self):
        """Test the help command in the console"""
        self.assertIn('help', dir(HBNBCommand), "HBNBCommand class is missing 'help' method")
        self.assertTrue(callable(getattr(HBNBCommand, 'help', None)), "'help' should be a method")

    def test_do_quit(self):
        """Test the do_quit command in the console"""
        self.assertIn('do_quit', dir(HBNBCommand), "HBNBCommand class is missing 'do_quit' method")
        self.assertTrue(callable(getattr(HBNBCommand, 'do_quit', None)), "'do_quit' should be a method")

    def test_do_EOF(self):
        """Test the do_EOF command in the console"""
        self.assertIn('do_EOF', dir(HBNBCommand), "HBNBCommand class is missing 'do_EOF' method")
        self.assertTrue(callable(getattr(HBNBCommand, 'do_EOF', None)), "'do_EOF' should be a method")


if __name__ == "__main__":
    unittest.main()

