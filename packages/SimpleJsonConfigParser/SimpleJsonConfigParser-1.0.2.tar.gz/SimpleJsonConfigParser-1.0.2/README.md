# SimpleJsonConfigParser

Module in python that allows easy creation, modification, and reading of JSON configuration files. This module aims to help make it easier to parse through config files and access the data within those configuration files from anywhere in your python program!


## Setup
Make sure to set a base directory and optionally a config directory. The base directory will tell the config reader where to search for the config file. Specifying a config path (combining the base directory and the name of the config) will be helpful when calling other methods.

These variable names DO NOT have to be 'base_directory' and 'config_path' just as long as a valid directory path and path the config you will create later with the create_config() method.

![image](https://github.com/TPosty/SimpleJsonConfigParser/assets/152321491/cd5b2d4d-0cf5-4d4e-8485-5376faa78933)

Please note that you do not have to specify a config path at the top of your python file. This is purely to show good practice in using a variable for the config file path if you ALREADY know the config name.

## Creating a configuration file
Configuration files are created using the `create_config()` method. This method takes in 1 argument, as well as an optional second argument. The first argument asks for the name of the configuration file and should be a string. If you would like to write information to the configuration file when it's created, you can pass a dictionary as the second argument and the dictionary will be written to the configuration file when it's created.

This is an example of what a default configuration dictionary would look like and how the method is called:

![image](https://github.com/TPosty/SimpleJsonConfigParser/assets/152321491/4e11a846-bc7a-4398-828b-41651f1b5e78)

If you end up passing in data when creating a configuration file, the `config.json` should look something like this:

![image](https://github.com/TPosty/SimpleJsonConfigParser/assets/152321491/34236632-77cc-4cae-9bb8-95ecdb0f7e7d)


## Adding Sections to a configuration file
In the context of this package, a "section" is referred to a key that has any number of nested key, value pairs inside of it. What makes a section different than other key, value pairs is that sections are at the root of the dictionary and typically describe the data inside of them. For example, a section called "Interface" could include configuration settings for a user interface within it.

To create a new section, use the `add_section()` method:

![image](https://github.com/TPosty/SimpleJsonConfigParser/assets/152321491/9d423c84-6b3d-4a52-848f-cf9e1ba2e643)

This method takes your configuration file path and the name of the section you want to add as arguments.

## Adding keys and values to sections
To add keys and values to already created sections, use the `add_key()` method. This method takes 4 arguments: configuration file path, the "parent" section, the key you want to add, the value you want to add:

![image](https://github.com/TPosty/SimpleJsonConfigParser/assets/152321491/d0f50c18-57c0-440f-8faf-8c740f440ad2)

## Removing keys and values from sections
To remove a key from a configuration file, use the `remove_key()` method. This method takes 3 arguments: configuration file path, the "parent" section, the key that you want to remove:

![image](https://github.com/TPosty/SimpleJsonConfigParser/assets/152321491/ce90c449-6293-4e23-8dda-6177b38468c5)

In the case you want to remove a key, you do not have to specify a value to be removed as the value will be removed with the associated key.
