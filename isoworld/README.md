# PROGRAMME . isoworld.py
Welcome to our post apocalyptic world!

Nous remercions a M. Bredeche pour nous fournir le code initial.

Notre concept est avoir un monde avec des zombies et des humains. En principe, le programme simule un combat entre les humains et zombies ou les humains ont des armes pour se proteger et ils peuvent s'enfuir mais en même temps, les zombies peuvent les chasser. Notre environnement est cree aleatoirement. 
Le sujet est mieux detaille dans le rapport.

Le code principal (appele isoworld.py) est dans le repertoire appele isoworld et pour l'executer il faut simplement taper dans terminal:
 cd isoworld
 python3 ./isoworld.py dans terminal 

 (peut varier selon les versions)

 La plupart des probabilites et les parametres du monde et du simulation sont au debut du code pour les faire varier.

 On a quelques versions du code pour facilement tester le code (pour avoir des exemplaires du fonctionnement du code ).  
 Risques des petit bugs etant donne que les programmes contiennent une petit partie du code original 
 - prison.py -> pour voir l'interaction objet-agent
 - agentsOnly.py -> un monde sans objets pour observer seulement les agents (basic et dropped)
 - boxingRing.py -> un monde petit avec un seul humain et un seul zombie pour observer le combat. (boucle infini jusqu'a 'esc')
 - droppedExample.py -> un monde avec un seul humain et beaucoup de food drops pour voir la fonction eat (tres similaire a gun et cure)

 Nous vous remercions 






INITIAL CODE :

World of Isotiles
=================

**Wofi** is a light-weight (non-optimised) implementation for creating isometric worlds. It features multi-level terrains with altitude, objects and agents. The code is primarily developed as a teaching material for the coding project on artificial life "2i013, projet: Vie Artificielle", part of the bachelor in computer science at Sorbonne Université (SU). This code is provided as an entry point to develop more complex projects including dynamic environments (e.g. forest fires, ecological changes) and species interactions (e.g. predator-prey dynamics, dynamic path planning), though you can probably develop simple games with it too.

* Author: *nicolas.bredeche(at)sorbonne-universite.fr*
* Started: *2018-11-17*
* Licence: CC-BY-SA -- *feel free to do whatever you want, but cite source.*

Installation and Running
========================

* **Dependencies**: Python3, Pygame
* **Running**: *python3 isoworld.py*

Snapshot
========

![Wofi screenshot](https://github.com/nekonaute/isoworld/blob/master/data/snapshot.png)

Credits for third party resources
=================================

**Assets**: https://www.kenney.nl/ (*great assets by Kenney Vleugels with public domain license*)

Benchmarking
============

Method:
* (1) in the console: **python3 demo_20181119_12h45.py**
* (2) wait for at least 3 FPS updates (see console), exit (press ESC in window), then record final line with fps count (line starts with "[Quit]")

Data:
* Macbook pro, Early 2015, 3.1ghz Intel Core i7, 16 GB RAM, Intel Iris Graphics 6100: 10.272582194960501 fps (2018-11-19, Nicolas)
* Ubuntu 18.04, Intel Xeon(R) CPU E5-2609 v4 @ 1.70GHz x 16, 32 Go, Quadro K420/PCIe/SSE2: 18.57459813310919 fps (2018-11-19, Paul)

*Hint: an efficient and quite easy way to optimise running speed is to redraw only cells that have changed inbetween updates, rather than the whole world (which is the current method).*
