# SSH-Connector 🚀

## Description

**SSH-Connector** est une application graphique en Python utilisant **PyQt5**, **paramiko** et **SCP** pour gérer les transferts de fichiers via SSH. Elle permet aux utilisateurs de se connecter à un serveur SSH (comme un Raspberry Pi), de transférer des fichiers, de naviguer dans les répertoires distants, et de supprimer ou télécharger des fichiers à distance.

L'application dispose d'une interface intuitive pour :
- Se connecter à un serveur SSH avec un nom d'utilisateur et un mot de passe.
- Visualiser, télécharger, envoyer et supprimer des fichiers sur le serveur distant.
- Naviguer dans les répertoires distants via une interface graphique.

## Fonctionnalités
- **Connexion SSH** : Se connecter à un serveur SSH à l'aide d'un nom d'utilisateur et d'un mot de passe.
- **Transfert de fichiers** : Télécharger et envoyer des fichiers depuis/vers le serveur.
- **Navigation dans les répertoires** : Accéder aux fichiers et répertoires distants.
- **Suppression de fichiers** : Supprimer des fichiers directement depuis l'application.
- **Rafraîchissement de la liste des fichiers** : Mettre à jour la liste des fichiers sur le serveur distant.

## 🛠️ Installation

### Prérequis
- Python 3.6+ installé sur votre machine.
- **PyQt5**, **paramiko** et **scp** sont nécessaires pour exécuter cette application.

Étapes d'installation
Clonez le dépôt :
```bash
git clone https://github.com/your-username/ssh-connector.git
cd ssh-connector
````
Installez les dépendances :
```bash
pip install -r requirements.txt
````

Lancez l'application :
```bash
python GUI.py
````

🎨 Apparence de l'application
L'application dispose d'une interface graphique simple et élégante avec des boutons arrondis et des couleurs attrayantes :

Bleu ciel pour un fond agréable.

Boutons bleu foncé avec une animation subtile au survol.

Listes de fichiers en vert sur fond noir pour faciliter la lisibilité.

📑 Code
Le projet utilise plusieurs bibliothèques Python pour la gestion de la connexion SSH et du transfert de fichiers :

paramiko : pour établir des connexions SSH et SFTP.

scp : pour transférer des fichiers via SCP.

PyQt5 : pour l'interface graphique.

APPARENCE :
<img width="1919" height="1031" alt="Capture d&#39;écran 2026-02-06 161652" src="https://github.com/user-attachments/assets/681ccee8-0941-4441-bd7d-26b606ab051d" />


🚀 Contribuer
Les contributions sont les bienvenues ! Si vous souhaitez améliorer l'application, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.
