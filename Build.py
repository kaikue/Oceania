#Original build script by Ryan Stillings- http://ryans.x10.mx/

from cx_Freeze import setup, Executable
import sys
import os
import fnmatch
import compileall
import shutil
import Game

base = None
if sys.platform == "win32":
	base = "Win32GUI"

excludes = []
includes = ["pygame"]
dirs = ["ent", "fnt", "gen", "gui", "img", "itm", "mus", "sfx"]

setup(name = "Oceania",version = Game.VERSION,description = "Underwater sandbox game",executables = [Executable("World.py", base = base, targetName="Oceania.exe")], options = {"build_exe": {"excludes":excludes, "includes":includes, "include_files":dirs}})

buildDirName = "Oceania-v" + Game.VERSION
buildPath = os.path.join(os.getcwd(),"build")
buildDirPath = os.path.join(buildPath,buildDirName)
#change default build folder name to project name
os.rename(os.path.join(buildPath,"exe.win-amd64-3.4"), buildDirPath)

#copy JSONs
jsons = ["biomes.json","blocks.json","items.json","structures.json"]
for json in jsons:
	shutil.copy(os.path.join(os.getcwd(),json), buildDirPath)

#copy OGG dlls
pygameDir = "C:\\Python34\\Lib\\site-packages\\pygame"
dlls = ["libogg.dll", "libvorbis.dll", "libvorbisfile.dll"]
for dll in dlls:
	shutil.copy(os.path.join(pygameDir,dll), buildDirPath)

#replace all .py files with compiled pyc files to speed up execution and reduce file size
for root, dirnames, filenames in os.walk(buildDirPath):
	for filename in fnmatch.filter(filenames, '*.py'): #replace all .py files with pre-compiled .pyc files
		curFile = os.path.join(root, filename)
		compileall.compile_file(curFile)
		os.remove(curFile)
		#python 3.4 will automatically change the extension from .py to .cpython-34.pyc, and move the file into a directory called __pycache__
		#move that file back out of the __pycache__ directory and replace the extension to simply .pyc
		os.rename(os.path.join(os.path.join(root,"__pycache__"),filename[:-3]+".cpython-34.pyc"),os.path.join(root,filename[:-3]+".pyc"))
		#if the __pycache__ folder is now empty (meaning either it was created when we compiled this file, or
		#it was created at some other time but never populated) delete it
		if not os.listdir(os.path.join(root,"__pycache__")):
			os.rmdir(os.path.join(root,"__pycache__"))