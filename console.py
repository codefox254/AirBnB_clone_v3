#!/usr/bin/python3
""" console """

import cmd
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # for splitting the line along spaces except in double quotes

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                obj = models.storage.get(classes[args[0]], args[1])
                if obj:
                    print(obj)
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                obj = models.storage.get(classes[args[0]], args[1])
                if obj:
                    models.storage.delete(obj)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representations of all instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_list = [str(obj) for obj in models.storage.all().values()]
        elif args[0] in classes:
            obj_list = [str(obj) for obj in models.storage.all(classes[args[0]]).values()]
        else:
            print("** class doesn't exist **")
            return False
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                obj = models.storage.get(classes[args[0]], args[1])
                if not obj:
                    print("** no instance found **")
                    return False
                if len(args) > 2:
                    if len(args) > 3:
                        setattr(obj, args[2], self._convert_type(args[3]))
                        obj.save()
                    else:
                        print("** value missing **")
                else:
                    print("** attribute name missing **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def _convert_type(self, value):
        """Converts a value to the appropriate type"""
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            count = models.storage.count(classes[args[0]])
            print(count)
        else:
            print("** class doesn't exist **")

    def default(self, arg):
        """Default method for the command interpreter"""
        args = arg.split('.')
        if len(args) < 2:
            print("*** Unknown syntax: {}".format(arg))
            return False
        class_name = args[0]
        method_call = args[1]
        if class_name in classes:
            if method_call.startswith("all()"):
                self.do_all(class_name)
            elif method_call.startswith("count()"):
                self.do_count(class_name)
            elif method_call.startswith("show("):
                id = method_call.split('"')[1]
                self.do_show("{} {}".format(class_name, id))
            elif method_call.startswith("destroy("):
                id = method_call.split('"')[1]
                self.do_destroy("{} {}".format(class_name, id))
            elif method_call.startswith("update("):
                params = method_call.split('(')[1].split(')')[0]
                params = params.replace('"', '').split(', ')
                self.do_update("{} {} {} {}".format(class_name, params[0], params[1], params[2]))
            else:
                print("*** Unknown syntax: {}".format(arg))
        else:
            print("*** Unknown syntax: {}".format(arg))


if __name__ == "__main__":
    HBNBCommand().cmdloop()

