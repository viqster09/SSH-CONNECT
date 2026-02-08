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

### SSH doit être activé sur votre serveur

**Important** : L'application nécessite que le service SSH soit activé sur votre serveur afin de permettre les connexions sécurisées via le protocole SSH. 

#### Sur un Raspberry Pi (par exemple) :
1. **Activer SSH** : Si SSH n'est pas déjà activé, vous devez l'activer via la commande suivante :
   ```bash
   sudo systemctl enable ssh
   sudo systemctl start ssh
Vérifier si SSH est actif :
   ```bash
   sudo systemctl status ssh

Configurer le pare-feu : Si vous avez un pare-feu actif, assurez-vous que le port 22 (par défaut pour SSH) est ouvert :

sudo ufw allow 22
Après avoir vérifié que SSH est activé sur votre serveur, vous pouvez vous connecter via l'application.

Étapes d'installation
Clonez le dépôt :

git clone https://github.com/your-username/ssh-connector.git
cd ssh-connector
Installez les dépendances :

pip install -r requirements.txt
Lancez l'application :

python app.py
📂 Utilisation
Se connecter à un serveur SSH
Ouvrez l'application.

Remplissez les champs de connexion avec l'adresse IP du serveur, le port, le nom d'utilisateur et le mot de passe.

Cliquez sur Se connecter pour établir une connexion SSH.

Une fois connecté, la liste des fichiers du serveur s'affichera dans la fenêtre.

Transfert de fichiers
Envoyer un fichier : Cliquez sur le bouton Envoyer un fichier, puis sélectionnez le fichier à envoyer. Le fichier sera transféré vers le répertoire actuel sur le serveur.

Télécharger un fichier : Sélectionnez un fichier dans la liste, puis cliquez sur Télécharger un fichier pour le télécharger sur votre machine locale.

Navigation dans les répertoires
Accéder aux sous-répertoires : Double-cliquez sur un dossier pour entrer dans le répertoire. Si vous êtes dans un répertoire limité (par exemple /home/user), l'accès à des répertoires parents est restreint.

Revenir au répertoire parent : Cliquez sur .. (Parent Directory) pour revenir au répertoire parent.

Supprimer un fichier
Sélectionnez un fichier dans la liste et cliquez sur Supprimer un fichier pour supprimer le fichier distant.

Rafraîchir la liste des fichiers
Cliquez sur le bouton Rafraîchir les fichiers pour mettre à jour la liste des fichiers du répertoire actuel sur le serveur.

Se déconnecter
Cliquez sur Se déconnecter pour fermer la connexion SSH et SFTP.

💻 Commandes SSH pour l'utilisation du serveur
Si vous devez configurer un utilisateur SSH ou transférer des fichiers manuellement, voici quelques commandes utiles :

Créer un nouvel utilisateur via SSH
Pour créer un nouvel utilisateur et lui attribuer un mot de passe :

sudo adduser newuser
sudo passwd newuser
Transfert de fichiers avec SCP
Envoyer un fichier vers le serveur :

scp localfile.txt user@hostname:/remote/path
Télécharger un fichier depuis le serveur :

scp user@hostname:/remote/path/remotefile.txt /local/path
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
