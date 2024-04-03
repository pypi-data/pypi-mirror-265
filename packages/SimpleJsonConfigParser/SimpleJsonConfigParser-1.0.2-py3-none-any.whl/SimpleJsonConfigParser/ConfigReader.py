import os
import json

class config_reader():

    def __init__(self, base_directory):
        self.base_directory = base_directory

    def create_config(self, config_name: str, *args):
        # Config file name (what to save the file as)
        # Path - Where to save the config file
        
        # First we need to check if a file with that name exists already on the user's OS
        if os.path.exists(os.path.join(self.base_directory, config_name)):
            print("Could not create the config due to the file already being there!")
            return
        else:
            # Proceed with the rest of the creation of the config file
            try:
                with open(os.path.join(self.base_directory, config_name), 'w') as config:
                    print("Created config file!")
                    # Check if there are other arguments, currently only supports argument for setup data.
                    if args:
                        try:
                            json_data = json.dumps(args[0], ensure_ascii=False, indent=4)
                            config.write(json_data)
                            config.close()
                            print("Found data passed as argument. Wrote data to config file successfully!")
                        except Exception as error:
                            print(error)
                    else:
                        config.write("{}")
                        config.close()
            except Exception as error:
                print(error)

    def add_section(self, config_path, section_key: str):
        valid_config = False

        if os.path.exists(config_path):
            valid_config = True
        else:
            valid_config = False

        new_data = {
            f"{section_key}": {}
        }
        # First need to make sure that the key is not already inside of the config file
        if valid_config:
            with open(config_path, 'r+') as config:
                try:
                    old_config_data = json.load(config)
                except json.decoder.JSONDecodeError:
                    old_config_data = {}
                    print("No config data so initialized with basic data.")
                

                if section_key in old_config_data:
                    print(f"The key: '{section_key}' was already present!")
                else:
                    try:
                        old_config_data.update(new_data)

                        config.seek(0)

                        json.dump(old_config_data, config, indent=4)

                        config.truncate()
                        print(f"Created new section: '{section_key}'")
                    except Exception as error:
                        print(error)
        else:
            print("Could not find the config path...")


    # Add a key, value pair to a config file.  
    def add_key(self, config_path, parent_section, key: str, value: any):
        valid_config = False

        # Checks to make sure that the config actually exists before making any modifications to it.
        if os.path.exists(config_path):
            valid_config = True
        else:
            valid_config = False
        
        if valid_config:
            with open(config_path, 'r+') as config:
                try:
                    old_config_data = json.load(config)
                except json.decoder.JSONDecodeError:
                    old_config_data = {}
                
                if parent_section in old_config_data:
                    # Need to fix the below so it actually works correctly...
                    if key in old_config_data[parent_section]:
                        print("Key already there!")
                    else:
                        old_config_data[parent_section][key] = value

                        config.seek(0)
                        json.dump(old_config_data, config, indent=4)
                        config.truncate()

                        print(f"Added key '{key}' with value '{value}' to section '{parent_section}'.")
                else:
                    print(f"Section: '{parent_section}' not found in the configuration!")

    # Remove specific key from config file.
    def remove_key(self, config_path, parent_section, key: str):
        valid_config = False

        # Checks to make sure that the config actually exists before making any modifications to it.
        if os.path.exists(config_path):
            valid_config = True
        else:
            valid_config = False
        
        if valid_config:
            with open(config_path, 'r+') as config:
                try:
                    old_config_data = json.load(config)
                except json.decoder.JSONDecodeError:
                    old_config_data = {}
                
                if parent_section in old_config_data:
                    # Need to fix the below so it actually works correctly...
                    if key in old_config_data[parent_section]:
                        old_config_data[parent_section].pop(key)

                        config.seek(0)
                        json.dump(old_config_data, config, indent=4)
                        config.truncate()

                        print(f"Removed key '{key}' from section '{parent_section}'.")
                    else:
                        print(f"Key: '{key}' already there!")
                else:
                    print(f"Section: '{parent_section}' not found in the configuration!")
            
    
    def remove_section(self, section_name: str):
        pass

    def get(self, config_path: str, parent_section: str, config_key: str):
        try:
            with open(config_path) as config:
                config_data = json.load(config)
                data = config_data[f'{parent_section}']
                for key, value in data.items():
                    if key == str(config_key):
                        return value
        except KeyError:
            print(f"Can't find one or more of the values specified in the config file: {parent_section}, {config_key}")
        except AttributeError:
            print("Please check to make sure the values specified in the config aren't strings.")
        except Exception as error:
            print(error)


