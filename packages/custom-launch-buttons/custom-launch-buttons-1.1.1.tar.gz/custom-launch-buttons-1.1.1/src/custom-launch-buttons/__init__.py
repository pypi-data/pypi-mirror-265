import os
import ruamel.yaml
import json


from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file


def copy_buttons(app: Sphinx, exc: None) -> None:
    print("[custom-launch-buttons] initialised, adding directories.")

    # directory paths 
    current_dir = os.path.dirname(__file__)
    staticdir = os.path.join(app.builder.outdir, '_static')
    
    # Define file paths
    js_file_path = os.path.join(current_dir, 'static', 'launch_buttons.js')
    launch_buttons_yaml = os.path.join(app.builder.srcdir, '_launch_buttons.yml')
    launch_buttons_json = os.path.join(staticdir, '_launch_buttons.json')
    
    # Convert _launch_buttons.yaml to _launch_buttons.json so it can be read in javascript
    yaml_to_json(launch_buttons_yaml, launch_buttons_json)

    print("[custom-launch-buttons] yaml converted to json")	

    if app.builder.format == 'html' and not exc:

        # Read the existing content of the JavaScript file
        with open(js_file_path, 'r') as js_file:
            existing_content = js_file.read()
        
        # Read the JSON object from the file
        with open(launch_buttons_json, 'r') as json_file:
            json_data = json.load(json_file)

        # Create a variable assignment with the JSON data
        variable_assignment = 'let _button_data = ' + json.dumps(json_data) + ';\n\n'

        new_content = variable_assignment + existing_content

        # Write the modified content back to the JavaScript file
        with open(js_file_path, 'w') as js_file:
            js_file.write(new_content)
        
        # Copy all files from static to output directory
        copy_asset_file(js_file_path, staticdir)
        copy_asset_file(launch_buttons_json, staticdir)
        copy_asset_file(launch_buttons_yaml, staticdir)
        
        print("[custom-launch-buttons] copied files to _static directory.")
        
        
# Function to convert yaml to json to prevent mixing of yaml and json for the user.
def yaml_to_json(yaml_file: str, json_file: str) -> None:
    with open(yaml_file, 'r') as ymlfile:
        yaml = ruamel.yaml.YAML(typ='safe')
        data = yaml.load(ymlfile)
        with open(json_file, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)

def setup(app: Sphinx) -> dict[str, str]:
    app.add_js_file('launch_buttons.js')
    app.connect('build-finished', copy_buttons)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
