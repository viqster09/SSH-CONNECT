import sys
import os
import paramiko
from scp import SCPClient
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QFormLayout, QListWidget, QMessageBox
from PyQt5.QtCore import Qt

class SSHFileTransferApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SSH File Transfer to Raspberry Pi")
        self.setGeometry(200, 200, 600, 400)

        self.ssh_client = None
        self.sftp_client = None
        self.current_path = '/home'  # Par défaut, répertoire de l'utilisateur admin
        self.username = None  # Le nom d'utilisateur connecté

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Form layout pour les informations de connexion
        form_layout = QFormLayout()

        # Champs de saisie pour IP, port, nom d'utilisateur, mot de passe
        self.ip_input = QLineEdit(self)
        self.port_input = QLineEdit(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Masquer le mot de passe

        # Placer les champs dans le layout
        form_layout.addRow("IP du serveur SSH:", self.ip_input)
        form_layout.addRow("Port:", self.port_input)
        form_layout.addRow("Nom d'utilisateur:", self.username_input)
        form_layout.addRow("Mot de passe:", self.password_input)

        layout.addLayout(form_layout)

        # Bouton pour se connecter via SSH
        self.connect_button = QPushButton("Se connecter", self)
        self.connect_button.clicked.connect(self.connect_to_ssh)
        layout.addWidget(self.connect_button)

        # Label d'état de la connexion
        self.status_label = QLabel("Non connecté", self)
        layout.addWidget(self.status_label)

        # Liste des fichiers présents sur le Raspberry Pi
        self.file_list = QListWidget(self)
        self.file_list.setSelectionMode(QListWidget.SingleSelection)
        self.file_list.itemDoubleClicked.connect(self.on_item_double_clicked)  # Gérer le double-clic
        layout.addWidget(self.file_list)

        # Bouton pour envoyer des fichiers
        self.upload_button = QPushButton("Envoyer un fichier", self)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        # Bouton pour télécharger des fichiers
        self.download_button = QPushButton("Télécharger un fichier", self)
        self.download_button.clicked.connect(self.download_file)
        layout.addWidget(self.download_button)

        # Bouton pour supprimer un fichier
        self.delete_button = QPushButton("Supprimer un fichier", self)
        self.delete_button.clicked.connect(self.delete_file)
        layout.addWidget(self.delete_button)

        # Bouton pour afficher les fichiers du Raspberry Pi
        self.refresh_button = QPushButton("Rafraîchir les fichiers", self)
        self.refresh_button.clicked.connect(self.refresh_file_list)
        layout.addWidget(self.refresh_button)

        # Bouton pour se déconnecter
        self.disconnect_button = QPushButton("Se déconnecter", self)
        self.disconnect_button.clicked.connect(self.disconnect_from_ssh)
        layout.addWidget(self.disconnect_button)

        self.setLayout(layout)

        # Appliquer les styles
        self.apply_styles()

    def apply_styles(self):
        style = """
        /* Style général */
        QWidget {
            background-color: #87CEEB;  /* Bleu ciel */
            font-family: Arial, sans-serif;
            color: white;
        }

        /* Boutons */
        QPushButton {
            background-color: #003366;  /* Bleu foncé */
            color: white;
            border-radius: 12px;  /* Boutons arrondis */
            padding: 10px;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #005bb5;  /* Bleu clair quand survolé */
        }

        QPushButton:pressed {
            background-color: #002a4d;  /* Couleur plus foncée quand appuyé */
        }

        /* Champs de saisie avec dégradé de bleu clair à bleu foncé */
        QLineEdit {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #87CEEB, stop:1 #003366);
            color: #333333;  /* Texte plus foncé pour une meilleure lisibilité */
            border: 2px solid #003366;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }

        /* Label */
        QLabel {
            font-size: 16px;
        }

        /* Liste des fichiers */
        QListWidget {
            background-color: black;  /* Fond noir pour la liste */
            color: green;  /* Texte en vert */
            font-size: 12px;
        }

        QListWidget:item {
            padding: 5px;
        }

        QListWidget:item:selected {
            background-color: #005bb5;  /* Bleu clair quand sélectionné */
            color: white;
        }

        /* Fond de la fenêtre principale */
        QWidget {
            border-radius: 10px;
        }

        /* Animation pour le bouton de connexion */
        QPushButton#connect_button {
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0% {
                background-color: #003366;
            }
            50% {
                background-color: #005bb5;
            }
            100% {
                background-color: #003366;
            }
        }
        """
        self.setStyleSheet(style)

    def connect_to_ssh(self):
        # Récupérer les informations de connexion depuis l'interface
        ip = self.ip_input.text()
        port = self.port_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not ip or not port or not username or not password:
            self.status_label.setText("Tous les champs doivent être remplis !")
            return

        try:
            # Connexion SSH
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(ip, port=int(port), username=username, password=password)

            # Connexion SFTP
            self.sftp_client = self.ssh_client.open_sftp()

            # Enregistrer le nom d'utilisateur pour gérer les permissions
            self.username = username
            self.status_label.setText(f"Connecté à {ip} sur le port {port}")

            # Définir le répertoire initial en fonction de l'utilisateur
            if username == "user":
                self.current_path = "/home/user"  # Limiter l'accès au répertoire de l'utilisateur
            elif username == "login":
                self.current_path = "/home/login"  # L'administrateur a accès à tout

            self.refresh_file_list()

        except Exception as e:
            self.status_label.setText(f"Erreur de connexion: {e}")

    def upload_file(self):
        # Ouvrir un dialogue pour choisir un fichier sur ton PC
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier", "", "Tous les fichiers (*)")

        if file_path:
            # Normaliser le chemin local pour éviter les erreurs de backslash sous Windows
            file_path = os.path.normpath(file_path)

            # Vérifie si c'est bien un fichier (pas un répertoire)
            if os.path.isfile(file_path):
                # Le chemin distant du fichier, avec le même nom de fichier dans le répertoire actuel
                remote_file_path = os.path.join(self.current_path, os.path.basename(file_path))
                remote_file_path = os.path.normpath(remote_file_path)

                try:
                    # Transférer le fichier avec SCP
                    self.transfer_file_with_scp(file_path, remote_file_path)
                    self.status_label.setText(f"Fichier {file_path} envoyé à {remote_file_path}")
                    self.refresh_file_list()  # Rafraîchir la liste après l'envoi
                except Exception as e:
                    self.status_label.setText(f"Erreur d'envoi : {e}")
            else:
                self.status_label.setText("Ce n'est pas un fichier valide.")

    def transfer_file_with_scp(self, local_file_path, remote_file_path):
        # Utiliser SCP pour transférer le fichier
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_file_path, remote_file_path)
        except Exception as e:
            raise Exception(f"Erreur lors du transfert SCP : {str(e)}")

    def refresh_file_list(self):
        # Rafraîchir la liste des fichiers sur le Raspberry Pi
        try:
            files = self.sftp_client.listdir(self.current_path)  # Liste les fichiers dans le répertoire actuel
            self.file_list.clear()
            # Ajouter '..' pour revenir au répertoire parent
            self.file_list.addItem(".. (Parent Directory)")
            for file in files:
                self.file_list.addItem(file)
            self.status_label.setText("Fichiers rafraîchis")
        except Exception as e:
            self.status_label.setText(f"Erreur lors du rafraîchissement : {e}")

    def on_item_double_clicked(self, item):
        # Lorsque l'utilisateur double-clique sur un élément
        file_name = item.text()

        if file_name == ".. (Parent Directory)":
            # Si on double-clique sur "..", on revient au répertoire parent
            self.go_back()
        else:
            # Vérifie si l'élément est un dossier et navigue dedans
            try:
                new_path = os.path.join(self.current_path, file_name)
                # Si c'est un répertoire, on met à jour le chemin et on rafraîchit
                if self.is_directory(new_path):
                    self.current_path = new_path
                    self.refresh_file_list()
            except Exception as e:
                self.status_label.setText(f"Erreur lors de l'ouverture du dossier : {e}")

    def is_directory(self, path):
        # Vérifier si le chemin est un répertoire
        try:
            command = f"sudo test -d {path} && echo 'yes' || echo 'no'"
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            result = stdout.read().decode('utf-8').strip()
            return result == 'yes'
        except Exception as e:
            return False

    def go_back(self):
        # Revenir au répertoire parent
        parent_path = os.path.dirname(self.current_path)

        # Si l'utilisateur est "user", ne pas remonter en dehors de /home/user
        if self.username == "user" and parent_path.startswith("/home/user"):
            self.current_path = parent_path
        elif self.username == "login" and parent_path != "/":
            self.current_path = parent_path
        elif self.username == "login" and parent_path == "/":
            self.current_path = "/home/login"  # Ne pas remonter au-delà de /home/admin pour l'admin

        self.refresh_file_list()  # Rafraîchir la liste des fichiers après le changement de répertoire

    def download_file(self):
        # Vérifier si un fichier est sélectionné
        current_item = self.file_list.currentItem()
        if not current_item:
            # Si aucun fichier n'est sélectionné, afficher une alerte
            QMessageBox.warning(self, "Alerte", "Veuillez sélectionner un fichier à télécharger.")
            return

        # Récupérer le fichier sélectionné
        file_name = current_item.text()

        # Si c'est "..", on ne fait rien
        if file_name == ".. (Parent Directory)":
            return

        remote_file_path = os.path.join(self.current_path, file_name)
        local_file_path, _ = QFileDialog.getSaveFileName(self, "Choisir un emplacement pour enregistrer le fichier", file_name)

        if local_file_path:
            try:
                # Télécharger le fichier depuis le Raspberry Pi
                self.sftp_client.get(remote_file_path, local_file_path)
                self.status_label.setText(f"Fichier téléchargé : {local_file_path}")
            except Exception as e:
                self.status_label.setText(f"Erreur lors du téléchargement : {e}")

    def delete_file(self):
        # Supprimer un fichier sélectionné depuis le Raspberry Pi
        if not self.sftp_client:
            self.status_label.setText("Non connecté !")
            return

        file_name = self.file_list.currentItem().text()

        # Si c'est "..", on ne fait rien
        if file_name == ".. (Parent Directory)":
            return

        remote_file_path = os.path.join(self.current_path, file_name)

        try:
            # Supprimer le fichier distant
            self.sftp_client.remove(remote_file_path)
            self.status_label.setText(f"Fichier {file_name} supprimé.")
            self.refresh_file_list()  # Rafraîchir la liste après suppression
        except Exception as e:
            self.status_label.setText(f"Erreur lors de la suppression : {e}")

    def disconnect_from_ssh(self):
        # Se déconnecter de la session SSH et SFTP
        if self.sftp_client:
            self.sftp_client.close()
            self.sftp_client = None

        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None

        self.status_label.setText("Déconnecté")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SSHFileTransferApp()
    window.show()
    sys.exit(app.exec_())
