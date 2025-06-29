## Author

Dickson Lee (2495196)

420-9420-VA: Application Development (PyQt6) 

29 June 2025

Denis Renfret

Vanier College – Final Project

# Pokédex Application (PyQt6 Final Project)

## Project Title
PyQt6 Pokedex

## Description

This is a desktop Pokédex application developed using Python and PyQt6 as a final project for the Application Development course. The program allows users to search for Pokémon by name or ID, view their stats, types, abilities, and optionally toggle shiny sprites. The goal is to simulate a clean and informative GUI-based tool modeled after the in-game Pokédex. The data are fetch with GET requests from PokéAPI(https://pokeapi.co/). The targeted audience is anyone who has a cultural passion for Pokémon. Again, the Pokédex application is designed to provide a user-friendly way to access Pokémon data using a clean graphical interface. The target users are Pokémon fans, students learning GUI development, and developers interested in working with APIs and PyQt6. It allows them to have simple Pokédex at their disposal whenever they are playing their beloved video game.

## Planned Features and Functionalities

- Search for Pokémon by name or ID using a QLineEdit and QPushButton
- Toggle shiny sprite display using a QCheckBox
- Display of Pokémon sprite image
- Detailed info panel with name, ID, types, abilities, groups, and base stats
- Detailed info panel with move
- Navigation buttons to go to the next or previous Pokémon
- Input validation and error message handling
- Menu bar with actions and shortcuts (if implemented)

## Meeting Technical Requirements
This project fulfills all the course's technical requirements:
- Multiple windows (main + optional settings/about)
- At least 6 widgets: QLineEdit, QPushButton, QLabel, QCheckBox, QTextEdit, QMessageBox
- At least 3 layout managers: QVBoxLayout, QHBoxLayout, QGridLayout
- Menu system and QAction setup with keyboard shortcuts
- Custom signals for shiny toggle or Pokémon navigation
- Input validation and try/except error handling
- Clear class structure and modularized codebase

## Technologies Used

- Python 3
- PyQt6
- Requests (for PokéAPI access)
- QtGui, QtWidgets, QtCore

## Widgets and Layouts Used

### Widgets:
- QMainWindow
- QLineEdit
- QPushButton
- QLabel
- QCheckBox
- QTextEdit or QPlainTextEdit

### Layouts:
- QVBoxLayout
- QHBoxLayout
- QGridLayout or nested layouts

## Custom Signals

- Signal for when a shiny toggle state changes
- Signal for next/previous Pokémon navigation

## Course Requirements Met

- Multiple windows or dialogs
- Use of at least 6 different PyQt6 widgets
- Use of at least 3 different layout managers
- Built-in and custom signal-slot mechanisms
- Menu system with actions and optional toolbar
- Keyboard shortcuts (if implemented)
- Data management using Python data structures
- File operations (if implemented)
- Input validation and error handling
- Clean code structure with documentation


