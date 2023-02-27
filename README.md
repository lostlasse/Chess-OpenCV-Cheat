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
   2. Change the stockfish path in the *config.json*<br>
   3. Replace the pictures of the figures in the *black* and *white* folders<br>
   
   https://user-images.githubusercontent.com/100237052/221702753-3d7b51da-d141-404f-96c4-dab0a72e5da3.mp4
   
   __Attention: The window size of the chess game must remain the same, as when the pictures were taken.__<br>
   4. Run the executable<br>
   5. Use the *X*, *Y* and the *Offset* sliders to math the grid<br>
   6. Position the *Off->On* slider to *On* to disable the positioning<br>
   7. Position the *calc* slider to *On* to calculate the next best move<br>
      If you run into an Error first check if all figures are detected.
