#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def process_input(input_arg):
    curly_match = re.search(r"\{(.*?)\}", input_arg)
    bracket_match = re.search(r"\[(.*?)\]", input_arg)
    if curly_match is None:
        if bracket_match is None:
            return [val.strip(",") for val in split(input_arg)]
        else:
            split_input = split(input_arg[:bracket_match.span()[0]])
            result_list = []
            for i in split_input:
                result_list.append(i.strip(","))
            result_list.append(bracket_match.group())
            return result_list
    else:
        split_input = split(input_arg[:curly_match.span()[0]])
        result_list = []
        for i in split_input:
            result_list.append(i.strip(","))
        result_list.append(curly_match.group())
        return result_list


class HBNBCommand(cmd.Cmd):
    """Defines the HBNB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def blank_line(self):
        """Do nothing upon receiving a blank line."""
        pass

    def end_of_file(self, arg):
        """Handle EOF signal to exit the program."""
        print("")
        return True

    def _quit(self, arg):
        """Quit command to exit the program."""
        return True

    def default_behavior(self, arg):
        """Default action for invalid input"""
        cmd_dict = {
            "all": self.display_all,
            "count": self.count_instances,
            "create": self.create_instance,
            "destroy": self.delete_instance,
            "show": self.display_instance,
            "update": self.update_instance
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                cmd = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if cmd[0] in cmd_dict.keys():
                    call_cmd = "{} {}".format(arg_list[0], cmd[1])
                    return cmd_dict[cmd[0]](call_cmd)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def display_all(self, input_arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arg_list = parse(input_arg)
        if len(input_list) > 0 and input_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            object_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    object_list.append(obj.__str__())
                elif len(input_list) == 0:
                    object_list.append(obj.__str__())
            print(object_list)

    def count_instances(self, input_arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        """
        input_list = process_input(input_arg)
        instance_count = 0
        for obj in storage.all().values():
            if input_list[0] == obj.__class__.__name__:
                instance_count += 1
        print(instance_count)

    def create_instance(self, input_arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        input_list = process_input(input_arg)
        if len(input_list) == 0:
            print("** class name missing **")
        elif input_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(input_list[0])()
            print(new_instance.id)
            storage.save()

    def delete_instance(self, input_arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arg_list = process_input(input_arg)
        object_dict = storage.all()
        if len(input_list) == 0:
            print("** class name missing **")
        elif input_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(input_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in object_dict.keys():
            print("** no instance found **")
        else:
            del object_dict["{}.{}".format(input_list[0], input_list[1])]
            storage.save()

    def display_instance(self, input_arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_list = process_input(input_arg)
        object_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in object_dict:
            print("** no instance found **")
        else:
            print(object_dict["{}.{}".format(arg_list[0], arg_list[1])])

    def update_instance(self, input_arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
           <class>.update(<id>, <attribute_name>, <attribute_value>) or
           <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        input_list = process_input(input_arg)
        object_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_list) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_list[0], arg_list[1]) not in object_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_list) == 4:
            obj = object_dict["{}.{}".format(arg_list[0], arg_list[1])]
            if arg_list[2] in obj.__class__.__dict__.keys():
                value_type = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = value_type(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = object_dict["{}.{}".format(arg_list[0], arg_list[1])]
            for k, value in eval(arg_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = value_type(value)
                else:
                    obj.__dict__[k] = value
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
