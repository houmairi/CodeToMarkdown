# Code Collector

This Python script creates a GUI application using the `tkinter` library for collecting code from selected files and saving it to a single output file. It also provides functionality to save and load profiles for easy reuse of selected directories and files.

## Features

- Select a directory and display its files and subdirectories in a tree view
- Add selected files to a separate tree view for collection
- Remove files from the selected files tree view
- Choose a save location for the output file
- Enter a filename for the output file
- Collect code from the selected files and save it to the output file
- Save profiles with selected directory, filename, save location, and selected files
- Load previously saved profiles

## Prerequisites

- Python 3.x
- `tkinter` library (usually included with Python)

## Usage

1. Run the script using Python:

   ```bash
   python CodeToMarkdown.py
   ```

2. Click the "Select" button next to the "Directory" entry to choose the directory containing the files you want to collect code from.

3. The files and subdirectories of the selected directory will be displayed in the left tree view.

4. Select the desired files from the left tree view and click the "Add" button to add them to the right tree view.

5. To remove files from the selected files tree view, select them and click the "Remove" button.

6. Enter a filename for the output file in the "Filename" entry (default is "output.txt").

7. Click the "Select" button next to the "Save Location" entry to choose the directory where the output file will be saved.

8. Click the "Collect Code" button to collect the code from the selected files and save it to the output file.

9. To save a profile, enter a profile name in the "Profile Name" entry and click the "Save Profile" button.

10. To load a previously saved profile, select it from the profile dropdown menu.

## File Structure
The script assumes the following file structure:
    ```bash
    - code_collector.py
    - profiles.json
    ```

-code_collector.py: The main Python script containing the code for the GUI application.
-profiles.json: A JSON file that stores the saved profiles.

## Dependencies
The script relies on the following Python libraries:

- os: For file and directory operations
- tkinter: For creating the GUI application
- json: For saving and loading profiles

These libraries are typically included with Python, so no additional installation is required.

## License
This script is open-source and available under the MIT License.

## Contributing
Contributions to the script are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## Acknowledgments
This script was created as a learning exercise and demonstrates the usage of the tkinter library for building GUI applications in Python.