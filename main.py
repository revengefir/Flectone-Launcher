import minecraft_launcher_lib
import subprocess

print("Welcome to Flectone Launcher A.0.3")

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace("minecraft", "flectone")

version = input("Enter minecraft version: ")
username = input("Enter username: ")

# Installing minecraft.
minecraft_launcher_lib.install.install_minecraft_version(versionid=version, minecraft_directory=minecraft_directory)

options = {
    'username': username,
    'uuid':'',
    'token': ''
}

subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=version, minecraft_directory=minecraft_directory,options=options))