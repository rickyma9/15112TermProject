# 15112TermProject

Project description:
Name: osu mini
Description: a rythmn game where you click circles to the beat of the song. you can also create your own beatmaps.
add circles so that you have to place stuff on those
add difficulty rating

Competitive analysis: 
My game is inspired by the online rythmn game OSU, which is a user-based game where you click circles to the beat of a song.
You can also make your own beatmaps, which is the only source of beatmaps for the game. My game will follow this format,
and I will try to emulate the UI of the game to make it complex. 

There will also be a small difference in that the user will be forced to place objects on two circles centered around the middle.

Structural Plan:
The project will be entirely based on OOP animation, where each object in the game is its own object (the circles and the sliders)
Each state of the game will also have its own class, and will be called based on different actions the user takes. 
(ex. welcome screen, game screen, pause screen, score screen)
Beatmaps will likely be an object which can be edited using methods in an EditBeatmap class.


Algorithmic plan:
The trickiest part of the project will likely be making the beatmap editor. In the beatmap editor, there will be features where
you place objects at different points in the song, and you can go back and change them whenever however you like.

How I will approach this part is most likely by allowing the user to use the scroll wheel and arrow keys to place objects at 
different points in the song. I will likely use lists or dictionaries to represent different points in the song,
and to represent what objects are present at that point in the song. I will also need to figure out how to allow people to 
import music files and create maps from those. I will also need to figure out how to keep the beatmap stored in an accesible 
location, which I can likely do using a list or set of beatmaps.

Timeline plan:
By 11/23: make better UI
By 11/24: Finish beatmap class
By 11/28: finish beatmap editor class
By 11/30: learn how to add cool effects
By 12/6: make really good UI

Version control plan:
Just using google drive and regularly backing up versions of the project in different folders in the drive

Module list:
pygame


current features:
1. generates circles that you can click and gain score based on when you click them.
there's an 'approach circle' that closes in over time, and the scoring is based on that


2. there are 'sliders' that you click and drag on. if your cursor goes outside of the 
range of the 'slider ball', then your combo resets to zero. currently, there is no
scoring for the sliders, it will come later.

in the future, there will be funcitonality so that you can time the placements 
of the circles and sliders to the beats of the song based on your own sense of rythmn.

3. plays music

4. displays an image


planned features:
1. beatmap editor - implemented

2. lock objects to circles - implemented

3. different screens - implemented

4. better UI - implemented
