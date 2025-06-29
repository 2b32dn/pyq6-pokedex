from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
    QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QTabWidget,
    QDialog, QProgressBar,QFileDialog
)
from PyQt6.QtGui import QAction, QPixmap, QKeySequence
from PyQt6.QtCore import Qt
import requests
import random


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Pokédex")
        self.setFixedSize(300, 200)

        mainBox = QVBoxLayout()
        mainBox.addWidget(QLabel("<b>Pokédex PyQt6</b>"))
        mainBox.addWidget(QLabel("Version 1.0"))
        mainBox.addWidget(QLabel("Created by Dickson Lee"))
        mainBox.addWidget(QLabel("Final Project for 420-942-VA"))
        mainBox.addWidget(QLabel("Data from PokéAPI (https://pokeapi.co)"))

        closeBtn = QPushButton("Close")
        closeBtn.clicked.connect(self.accept)
        mainBox.addWidget(closeBtn)

        self.setLayout(mainBox)


class EvolutionDialog(QDialog):
    def __init__(self, pokemonId):
        super().__init__()
        self.setWindowTitle("Evolution Chain")

        mainBox = QVBoxLayout()
        self.setLayout(mainBox)

        try:
            speciesUrl = f"https://pokeapi.co/api/v2/pokemon-species/{pokemonId}"
            speciesData = requests.get(speciesUrl).json()
            evo_url = speciesData["evolution_chain"]["url"]
            evolutionData = requests.get(evo_url).json()

            chain = evolutionData["chain"]
            while chain:
                name = chain["species"]["name"].capitalize()
                pokemonData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}").json()
                pokemonSpriteUrl = pokemonData["sprites"]["front_default"]
                imgLabel = QLabel()
                if pokemonSpriteUrl:
                    imgData = requests.get(pokemonSpriteUrl).content
                    pixmap = QPixmap()
                    pixmap.loadFromData(imgData)
                    imgLabel.setPixmap(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
                nameLabel = QLabel(name)
                nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

                mainBox.addWidget(imgLabel)
                mainBox.addWidget(nameLabel)

                if chain["evolves_to"]:
                    chain = chain["evolves_to"][0]
                else:
                    break
        except Exception as e:
            mainBox.addWidget(QLabel(f"Failed to load evolution chain.\n{e}"))

        closeBtn = QPushButton("Close")
        closeBtn.clicked.connect(self.accept)
        mainBox.addWidget(closeBtn)


class PokedexWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokédex")
        self.setGeometry(200, 200, 550, 700)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Enter Pokémon name or ID")
        self.searchInput.returnPressed.connect(lambda: self.searchPokemon())

        self.searchBtn = QPushButton("Search")
        self.searchBtn.clicked.connect(lambda: self.searchPokemon())

        self.randomBtn = QPushButton("Randomizer or Ctrl+R")
        self.randomBtn.clicked.connect(self.loadRandomPokemon)

        self.shinyCheckbox = QCheckBox("Show Shiny")
        self.shinyCheckbox.stateChanged.connect(lambda: self.searchPokemon())

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.infoTextLabel = QLabel()
        self.infoTextLabel.setWordWrap(True)
        self.infoTextLabel.setStyleSheet("color: white; font-size: 13px;")

        self.imageInfoLayout = QHBoxLayout()
        self.imageInfoLayout.addWidget(self.imageLabel, 1)
        self.imageInfoLayout.addWidget(self.infoTextLabel, 2)

        self.tabs = QTabWidget()

        self.infoDisplay = QTextEdit()
        self.infoDisplay.setReadOnly(True)

        self.movesDisplay = QTextEdit()
        self.movesDisplay.setReadOnly(True)

        self.typeEffectivenessDisplay = QTextEdit()
        self.typeEffectivenessDisplay.setReadOnly(True)

        self.tabs.addTab(self.infoDisplay, "Info")
        self.tabs.addTab(self.movesDisplay, "Moves")
        self.tabs.addTab(self.typeEffectivenessDisplay, "Type Effectiveness")

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.searchInput)
        topLayout.addWidget(self.searchBtn)
        topLayout.addWidget(self.randomBtn)

        self.leftBtn = QPushButton("◀")
        self.rightBtn = QPushButton("▶")
        self.leftBtn.clicked.connect(self.loadPreviousPokemon)
        self.rightBtn.clicked.connect(self.loadNextPokemon)

        navLayout = QHBoxLayout()
        navLayout.addWidget(self.leftBtn)
        navLayout.addWidget(self.rightBtn)

        self.savebtn = QPushButton("Save Info")
        self.savebtn.clicked.connect(self.save_pokemon_info)

        self.evolutionBtn = QPushButton("Show Evolution Chain")
        self.evolutionBtn.clicked.connect(self.showEvolutionDialog)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        shinyLayout = QHBoxLayout()
        shinyLayout.addWidget(self.shinyCheckbox)
        shinyLayout.addWidget(self.savebtn)
        shinyLayout.addWidget(self.evolutionBtn)
        mainLayout.addLayout(shinyLayout)
        mainLayout.addLayout(self.imageInfoLayout)
        # mainLayout.addWidget(self.evolutionBtn)
        mainLayout.addWidget(self.tabs)
        mainLayout.addLayout(navLayout)

        centralWidget.setLayout(mainLayout)

        self.currentId = 1
        self.init_menu()

    def init_menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        helpMenu = menubar.addMenu("Help")

        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(self.showAbout)
        aboutAction.setShortcut(QKeySequence("Ctrl+I"))
        helpMenu.addAction(aboutAction)
        
        randomizer = QAction("Random Pokémon", self)
        randomizer.setShortcut(QKeySequence("Ctrl+R"))
        randomizer.triggered.connect(self.loadRandomPokemon)
        fileMenu.addAction(randomizer)

    def showAbout(self):
        dialog = AboutDialog()
        dialog.exec()

    def showEvolutionDialog(self):
        dialog = EvolutionDialog(self.currentId)
        dialog.exec()

    def searchPokemon(self, nameOrId=None):
        if nameOrId is None:
            nameOrId = self.searchInput.text().strip().lower()

        if not nameOrId:
            QMessageBox.warning(self, "Input Error", "Please enter a Pokémon name or ID.")
            return

        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nameOrId}")
            if response.status_code != 200:
                raise ValueError("Pokémon not found")
            data = response.json()

            speciesResponse = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{data['id']}")
            if speciesResponse.status_code != 200:
                raise ValueError("Species not found")
            speciesData = speciesResponse.json()

            self.currentId = data['id']
            self.searchInput.setText(data['name'].capitalize())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            return

        toggleShiny = self.shinyCheckbox.isChecked()
        pokemonSpriteUrl = data["sprites"]["front_shiny"] if toggleShiny else data["sprites"]["front_default"]
        if pokemonSpriteUrl:
            imageData = requests.get(pokemonSpriteUrl).content
            pixmap = QPixmap()
            pixmap.loadFromData(imageData)
            self.imageLabel.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.imageLabel.clear()


        name = data["name"].capitalize()
        description = next((description["flavor_text"] for description in speciesData["flavor_text_entries"]
                            if description["language"]["name"] == "en"), "No description available.").replace("\n", " ").replace("\f", " ")
        types = [type["type"]["name"].capitalize() for type in data["types"]]
        abilities = [ability["ability"]["name"].replace("-", " ").capitalize() for ability in data["abilities"]]
        stats = {stat["stat"]["name"].capitalize(): stat["base_stat"] for stat in data["stats"]}

        eggGroups = speciesData.get('eggGroups', [])
        groupDisplay = ', '.join([group['name'].capitalize() for group in eggGroups]) if eggGroups else "Legendary"
        
        typeHexcodeMap = {
            "fire": "#EE8130",
            "water": "#6390F0",
            "grass": "#7AC74C",
            "electric": "#F7D02C",
            "ice": "#96D9D6",
            "fighting": "#C22E28",
            "poison": "#A33EA1",
            "ground": "#E2BF65",
            "flying": "#A98FF3",
            "psychic": "#F95587",
            "bug": "#A6B91A",
            "rock": "#B6A136",
            "ghost": "#735797",
            "dragon": "#6F35FC",
            "dark": "#705746",
            "steel": "#B7B7CE",
            "fairy": "#D685AD",
            "normal": "#A8A77E",
            "unknown": "#68A090",
            "shadow": "#000000"
        }
        genus = next((genus['genus'] for genus in speciesData['genera'] if genus['language']['name'] == 'en'), "Unknown Genus")
        self.infoTextLabel.setText(
            f"<h2 style='margin:0;'>{name}</h2>"
            f"<p style='margin:0;'>Species: {genus}</p>"
            f"<p>{description}</p>"
        )
        info = f"<div>"
        info += f"<h2>Pokémon data</h2>"
        info += f"<p>National #: {data['id']}</p>"
        info += f"<p>Types:</p>"
        for type in types:
            hexcode = typeHexcodeMap.get(type.lower(), "#ccc")
            info += (
                f"<span style=\"background-color: {hexcode}\";>&nbsp;&nbsp;{type}&nbsp;&nbsp;</span>&nbsp;"
            )
        info += f"<p>Height: {data['height'] / 10} m </p>"
        info += f"<p>Weight: {data['weight'] / 10} kg </p>"
        info += f"</div>"
        
        info += f"<h2>Abilities</h2>"
        for index, ability in enumerate(abilities):
            if index == 0:
                info += f"<p>{ability}</p>"
            else:
                info += f"<p>{ability} (Hidden Ability)</p>"
                
        info += f"<h2>Base Stats</h2>"
        for stat, val in stats.items():
            info += f"<div>{stat.replace('-', ' ')}</div>: {val}"
            
        info += f"<h2>Training</h2>"
        info += f"<p>Base Experience Yield: {data['base_experience']}</p>"
        info += f"<p>Base Happiness: {speciesData['base_happiness']}</p>"
        info += f"<p>Base Experience: {data['base_experience']}</p>"
        info += f"<p>Capture Rate: {speciesData['capture_rate']}</p>"
        info += f"<p>Growth Rate: {speciesData['growth_rate']['name'].capitalize().replace("-", " ")}</p>"
        
        info += f"<h2>Breeding</h2>"
        info += f"<p>Egg Groups: {groupDisplay}</p>"
        
        self.infoDisplay.setHtml(info)
        
        
        levelUpMovesList = set()
        machineMovesList = set()
        eggMovesList = set()

        for move in data["moves"]:
            moveName = move["move"]["name"].replace("-", " ").capitalize()
            for detail in move["version_group_details"]:
                method = detail["move_learn_method"]["name"]
                if method == "level-up":
                    levelUpMovesList.add(moveName)
                elif method == "machine":
                    machineMovesList.add(moveName)
                elif method == "egg":
                    eggMovesList.add(moveName)

        levelUpMoves = sorted(levelUpMovesList)
        machineMoves = sorted(machineMovesList)
        eggMoves = sorted(eggMovesList)

        moves_text = "Level-Up Moves:\n" + "\n".join(levelUpMoves) + "\n\n"
        moves_text += "TM Moves:\n" + "\n".join(machineMoves) + "\n\n"
        moves_text += "Egg Moves:\n" + "\n".join(eggMoves)
        self.movesDisplay.setPlainText(moves_text)


        self.displayTypeEffectiveness([t["type"]["url"] for t in data["types"]])

    def displayTypeEffectiveness(self, typeUrls):
        damageRelations = {
            "double_damage_from": set(),
            "half_damage_from": set(),
            "no_damage_from": set()
        }

        for url in typeUrls:
            try:
                typeData = requests.get(url).json()
                for key in damageRelations.keys():
                    for type in typeData["damageRelations"][key]:
                        damageRelations[key].add(type["name"].capitalize())
            except:
                continue

        weaknesses = ", ".join(sorted(damageRelations["double_damage_from"])) or "None"
        resistances = ", ".join(sorted(damageRelations["half_damage_from"])) or "None"
        immunities = ", ".join(sorted(damageRelations["no_damage_from"])) or "None"

        effectivenessText = f"Weak To (2x): {weaknesses}\n"
        effectivenessText += f"Resistant To (0.5x): {resistances}\n"
        effectivenessText += f"Immune To (0x): {immunities}"

        self.typeEffectivenessDisplay.setPlainText(effectivenessText)

    def loadNextPokemon(self):
        nextId = self.currentId + 1
        if nextId > 1025:
            nextId = 1
        self.searchPokemon(nextId)

    def loadPreviousPokemon(self):
        previousId = self.currentId - 1
        if previousId < 1:
            previousId = 1025
        self.searchPokemon(previousId)

    def loadRandomPokemon(self):
        randomId = random.randint(1, 1025)
        self.searchPokemon(randomId)

    def save_pokemon_info(self):
        if not self.infoDisplay.toPlainText():
            QMessageBox.warning(self, "No Data", "No Pokémon info to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Info", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(self.infoDisplay.toPlainText())
                QMessageBox.information(self, "Saved", f"Info saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file.\n{e}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = PokedexWindow()
    window.show()
    sys.exit(app.exec())
