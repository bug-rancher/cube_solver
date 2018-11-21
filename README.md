# Cube Solver

## Link
[http://bugrancher.pythonanywhere.com/](http://bugrancher.pythonanywhere.com/)

## About
This is a simple on-line application for solving Rubik's Cube. It's a implementation of Layer by Layer algorithm.

## Convention
All cube layouts in solver are representation of the cube made by "unfolding box" (or Third Angle Projection, or U.S. manufacturing drawings style).

<p align="center">
<img src="https://i0.wp.com/www.vista-industrial.com/blog/wp-content/uploads/2014/05/Figure-2-Third-Angle-Projection-in-a-Glass-Cube.png">
  <br>
  <i>source: www.vista-industrial.com</i>
</p>

## How it works
1. First you need orient your cube according to layout scheme - green centre in front of you, white centre on top of the cube and yellow centre on bottom of the cube.
2. Input colours of all sticker of your cube to the layout scheme. Click on colour in bottom row, and then click adequate stickers on scheme.
3. When you input all colours, click "solve".
4. Application check if you don't made a mistake during input by check if:
   * centres are not repeated
   * all stickers ale coloured
   * all edges are correct
   * edges are not repeated
   * all corners are correct
   * corners are not repeated
5. If application find a mistake, appear layout with marked bad element and description of error. Correct marked element on scheme and click "solve" again.
6. If all input is ok, application present a step by step solution to solve your cube. Every step is described by using Rubik's Cube Notation, and effect of this move is represent by layout. If you made all moves correctly, you solve your cube.

## Extras
1. For made things easier for people who doesn't know Rubik's Cube Notation, it will be described all the time on the screen next to solution.
2. If you want to change colours of centres on scheme (e.g. you really want to have red colour on top face), you can do this. Just remember to keep the convention of "unfolded box" and don't mess up faces position.

## Screens
Empty layout scheme:
![screen 01](https://user-images.githubusercontent.com/42303256/46002002-1b9dc600-c0ad-11e8-999e-1f7df06ee30e.png)

Layout scheme during input:
![screen 02](https://user-images.githubusercontent.com/42303256/46002003-1c365c80-c0ad-11e8-80e5-f2a8a880c498.png)

Layout scheme with detected errors:
![screen 03](https://user-images.githubusercontent.com/42303256/46002004-1c365c80-c0ad-11e8-8970-8c12bafa9d8a.png)

Step by step solution:
![screen 04](https://user-images.githubusercontent.com/42303256/46002005-1c365c80-c0ad-11e8-8819-432c12b49749.png)
