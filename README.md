# Chess-OpenCV-Cheat
A python script that can use object recognition to calculate the smartest move.

![Preview](https://user-images.githubusercontent.com/100237052/221702814-32e00b02-61c0-42a6-b2c7-94e6827aa89d.png)

## Dependencies
- [Stockfish](https://stockfishchess.org/download/)
- Python Dependencies (only if using source files):
  - [opencv2](https://pypi.org/project/opencv-python/)
  - [numpy](https://pypi.org/project/numpy/)
  - [pyautogui](https://pypi.org/project/PyAutoGUI/)
  - [mss](https://pypi.org/project/mss/)
  - [screeninfo](https://pypi.org/project/screeninfo/)
  - [stockfish](https://pypi.org/project/stockfish/)

## Setup
### Using the .exe release:
   1. Install Stockfish<br>
   2. Change the stockfish path in the *config.json*. You have to replace `\` with `\\`.<br>
   3. Replace the pictures of the figures in the *black* and *white* folders. For the best results, you should try to capture all of the figures against the same background color.<br>
   
   <img src="https://user-images.githubusercontent.com/100237052/222766347-d51f3bc6-5b3b-4562-8db5-4bc0b0c1f9c7.gif" />

   __Attention: The window size of the chess game must remain the same, as when the pictures were taken.__<br>
   4. Run the executable<br>
   5. Use the *X*, *Y* and the *Offset* sliders to math the grid<br>
   6. If your figures are black, change the *W->B* to B for black<br>
   7. Position the *Off->On* slider to *On* to disable the positioning<br>
   8. Position the *calc* slider to *On* to calculate the next best move<br>
      If you run into an Error first check if all figures are detected.<br>
      If not then you could try to change the *confidence* value.

## GUI
`X-Coord` : X-coordinate of the captured area<br>
`Y-Coord` : Y-coordinate of the captured area<br>
`X-Offset` : X offset of the captured area<br>
`Y-Offset` : Y offset of the captured area<br>
`Confidence` : The accuracy of character recognition<br>
`W->B` : Choose your color (W for white, B for black)<br>
`auto-move` : Turn off auto move. If activated, the script automatically moves the figures. But you still have to press *calc*.<br>
`Off->On` : Switching on deactivates the transformation mode<br>
`calc` : Turn on to calculate the next move. Note: The slider is reset to Off after each successful calculation or after an error.

## [Tutorial](http://www.youtube.com/watch?v=lXq4fEKAyIQ)


---
 - <a href="https://www.flaticon.com/free-icons/chess-pieces" title="chess pieces icons">Chess pieces icons created by VectorPortal - Flaticon</a>