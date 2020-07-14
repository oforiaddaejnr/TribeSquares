import sys
import simpleaudio as sa
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QPoint

CELL_COUNT = 8
CELL_SIZE = 50
GRID_ORIGINX = 175
GRID_ORIGINY = 175

class TribeSquares(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(150, 150, 700, 700)
        self.setWindowTitle('Tribe Squares')
        self.__x = -1
        self.__y = -1
        self.turn = 0
        self.empty = -1
        self.board = [[ self.empty for row in range(8)] for col in range(8)]
        self.checkGreenSquares = list()
        self.checkYellowSquares = list()
        self.greenmultiplier = 1
        self.yellowmultiplier = 1
        self.greenScore = 0
        self.yellowScore = 0
        self.counter = 0
        self.show()

    def gameOver(self):
        wave_obj = sa.WaveObject.from_wave_file('game_over.wav')
        play_obj = wave_obj.play()
        play_obj.wait_done() #causes lag


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                qp.setPen(QPen(Qt.black,0))
                qp.drawRect(col*CELL_SIZE + GRID_ORIGINX, row*CELL_SIZE + GRID_ORIGINY, CELL_SIZE, CELL_SIZE)
                if self.board[row][col] == 0:
                    xcoord = (GRID_ORIGINX+10) + col * CELL_SIZE
                    ycoord = (GRID_ORIGINY+10) + row * CELL_SIZE
                    greenInk = QColor("green")
                    qp.setPen(greenInk)
                    qp.setBrush(greenInk)
                    qp.drawRect(xcoord, ycoord, 30, 30)
                    qp.setBrush(QColor(Qt.transparent))

                elif self.board[row][col] == 1:
                    xcoord = (GRID_ORIGINX+10) + col * CELL_SIZE
                    ycoord = (GRID_ORIGINY+10) + row * CELL_SIZE
                    yellowInk = QColor("yellow")
                    qp.setPen(yellowInk)
                    qp.setBrush(yellowInk)
                    qp.drawRect(xcoord, ycoord, 30, 30)
                    qp.setBrush(QColor(Qt.transparent))

        print("counter =",self.counter)

        if self.counter == 64 and 0<=(self.__x - GRID_ORIGINY)// CELL_SIZE <8 and 0<=(self.__y - GRID_ORIGINY)// CELL_SIZE <8:
            qp.setPen(QColor("red"))
            qp.drawText(175, 155, "Game Over!!") #There is a lag before this prints because of the audio file
            self.gameOver()
            if self.greenScore > self.yellowScore:
                qp.drawText(300, 155, "Player 1 wins!")
            elif self.greenScore == self.yellowScore:
                qp.drawText(300, 155, "It's a tie!")
            else:
                qp.drawText(300, 155, "Player 2 wins!")


        if self.turn == 0 and self.counter != 64:
            qp.setPen(QColor("green"))
            qp.drawText(370, 600, "Player 1 Go!")
        elif self.turn == 1 and self.counter != 64:
            qp.setPen(QColor("yellow"))
            qp.drawText(370, 620, "Player 2 Go!")

        for group in range(len(self.checkGreenSquares)):
                qp.setPen(QColor("green"))
                qp.drawLine(GRID_ORIGINX+(self.checkGreenSquares[group][1]*50)+25, GRID_ORIGINY+(self.checkGreenSquares[group][0]*50)+25,GRID_ORIGINX+(self.checkGreenSquares[group][3]*50)+25, GRID_ORIGINY+(self.checkGreenSquares[group][2]*50)+25 )
                qp.drawLine(GRID_ORIGINX+(self.checkGreenSquares[group][3]*50)+25, GRID_ORIGINY+(self.checkGreenSquares[group][2]*50)+25,GRID_ORIGINX+(self.checkGreenSquares[group][5]*50)+25, GRID_ORIGINY+(self.checkGreenSquares[group][4]*50)+25 )
                qp.drawLine(GRID_ORIGINX+(self.checkGreenSquares[group][5]*50)+25, GRID_ORIGINY+(self.checkGreenSquares[group][4]*50)+25,GRID_ORIGINX+(self.checkGreenSquares[group][7]*50)+25, GRID_ORIGINY+(self.checkGreenSquares[group][6]*50)+25 )
                qp.drawLine(GRID_ORIGINX+(self.checkGreenSquares[group][7]*50)+25, GRID_ORIGINY+(self.checkGreenSquares[group][6]*50)+25,GRID_ORIGINX+(self.checkGreenSquares[group][1]*50)+25, GRID_ORIGINY+(self.checkGreenSquares[group][0]*50)+25 )
        for group in range(len(self.checkYellowSquares)):
                qp.setPen(QColor("yellow"))
                qp.drawLine(GRID_ORIGINX+(self.checkYellowSquares[group][1]*50)+25, GRID_ORIGINY+(self.checkYellowSquares[group][0]*50)+25,GRID_ORIGINX+(self.checkYellowSquares[group][3]*50)+25, GRID_ORIGINY+(self.checkYellowSquares[group][2]*50)+25 )
                qp.drawLine(GRID_ORIGINX+(self.checkYellowSquares[group][3]*50)+25, GRID_ORIGINY+(self.checkYellowSquares[group][2]*50)+25,GRID_ORIGINX+(self.checkYellowSquares[group][5]*50)+25, GRID_ORIGINY+(self.checkYellowSquares[group][4]*50)+25 )
                qp.drawLine(GRID_ORIGINX+(self.checkYellowSquares[group][5]*50)+25, GRID_ORIGINY+(self.checkYellowSquares[group][4]*50)+25,GRID_ORIGINX+(self.checkYellowSquares[group][7]*50)+25, GRID_ORIGINY+(self.checkYellowSquares[group][6]*50)+25 )
                qp.drawLine(GRID_ORIGINX+(self.checkYellowSquares[group][7]*50)+25, GRID_ORIGINY+(self.checkYellowSquares[group][6]*50)+25,GRID_ORIGINX+(self.checkYellowSquares[group][1]*50)+25, GRID_ORIGINY+(self.checkYellowSquares[group][0]*50)+25 )

        qp.setPen(QColor("green"))
        qp.drawText(270, 600, str(self.greenScore))
        qp.drawText(280, 600, "       X"+str(self.greenmultiplier))
        qp.setPen(QColor("black"))
        qp.drawText(270, 620, str(self.yellowScore))
        qp.drawText(280, 620, "       X"+str(self.yellowmultiplier))

        qp.end()

    def match(self, r,c):
        green_length = len(self.checkGreenSquares)
        yellow_length = len(self.checkYellowSquares)
        initialScore1 = self.greenScore
        initialScore2 = self.yellowScore
        for row in range (len(self.board)):
            for col in range (len(self.board[0])):
                #unrotated squares
                if c == col and r > row:
                    deltax = r - row
                    p3x = row
                    p3y = col - deltax
                    p4x = r
                    p4y = c - deltax
                    if p3y >= 0 and p4y >= 0:
                        if self.board[r][c] == self.board[row][col] == self.board[p3x][p3y]== self.board[p4x][p4y] != -1:
                            if self.turn == 0:
                                self.checkGreenSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (deltax + 1)**2
                            else:
                                print(deltax, row, col, p4x, p4y)
                                self.checkYellowSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.yellowScore += (deltax + 1)**2
                            print("Case 1")
                if c > col and r == row:
                    deltax = c - col
                    p3x = row + deltax
                    p3y = col
                    p4x = r + deltax
                    p4y = c
                    if p3x <= 7 and p4x <= 7:
                        if self.board[r][c] == self.board[row][col] == self.board[p3x][p3y]== self.board[p4x][p4y] != -1:
                            if self.turn == 0:
                                self.checkGreenSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (deltax + 1)**2
                            else:
                                self.checkYellowSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.yellowScore += (deltax + 1)**2
                            print("Case 2")
                if c == col and row > r:
                    deltay = row - r
                    p3x = row
                    p3y = col + deltay
                    p4x = r
                    p4y = c + deltay
                    if p3y <= 7 and p4y <= 7:
                        if self.board[r][c] == self.board[row][col] == self.board[p3x][p3y]== self.board[p4x][p4y] != -1:
                            if self.turn == 0:
                                self.checkGreenSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (deltay + 1)**2
                            else:
                                self.checkYellowSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.yellowScore += (deltay + 1)**2
                            print("Case 3")

                if col > c and row == r:
                    deltay = col - c
                    p3x = row - deltay
                    p3y = col
                    p4x = r - deltay
                    p4y = c
                    if p3x >= 0 and p4x >= 0:
                        if self.board[r][c] == self.board[row][col] == self.board[p3x][p3y]== self.board[p4x][p4y] != -1:
                            if self.turn == 0:
                                self.checkGreenSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (deltay + 1)**2
                            else:
                                self.checkYellowSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (deltay + 1)**2
                            print("Case 4")

                #rotated squares
                if col > c and row > r:
                    deltay = col - c
                    deltax = row - r
                    p3x = row + deltay
                    p3y = col - deltax
                    p4x = r + deltay
                    p4y = c - deltax
                    if p3x <= 7 and p3y >=0 and p4x <= 7 and p4y >= 0:
                        if self.board[r][c] == self.board[row][col] == self.board[p3x][p3y]== self.board[p4x][p4y] != -1:
                            if self.turn == 0:
                                self.checkGreenSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (max(deltax, deltay)+1)**2
                            else:
                                self.checkYellowSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.yellowScore += (max(deltax, deltay)+1)**2
                            print("Case 5")
                if c > col and r < row:
                    deltay = c - col
                    deltax = row - r
                    p3x = row - deltay
                    p3y = col - deltax
                    p4x = r - deltay
                    p4y = c - deltax
                    if p3x >= 0 and p3y >= 0 and p4x >= 0 and p4y >= 0:
                        if self.board[r][c] == self.board[row][col] == self.board[p3x][p3y]== self.board[p4x][p4y] != -1:
                            if self.turn == 0:
                                self.checkGreenSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (max(deltax, deltay)+1)**2
                            else:
                                self.checkYellowSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.yellowScore += (max(deltax, deltay)+1)**2
                            print("Case 6")
                if c > col and r > row:
                    deltay = c - col
                    deltax = r - row
                    p3x = row - deltay
                    p3y = col + deltax
                    p4x = r - deltay
                    p4y = c + deltax
                    if p3x >= 0 and p3y <= 7 and p4x >= 0 and p4y <= 7:
                        if self.board[r][c] == self.board[row][col] == self.board[p3x][p3y]== self.board[p4x][p4y] != -1:
                            if self.turn == 0:
                                self.checkGreenSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (max(deltax, deltay)+1)**2
                            else:
                                self.checkYellowSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.yellowScore += (max(deltax, deltay)+1)**2
                            print("Case 7")
                if col > c and row < r:
                    deltax = r - row
                    deltay = col - c
                    p3x = row + deltay
                    p3y = col + deltax
                    p4x = r + deltay
                    p4y = c + deltax
                    if p3x <= 7 and p3y <= 7 and p4x <= 7 and p4y <= 7:
                        if self.board[r][c] == self.board[row][col] == self.board[p3x][p3y]== self.board[p4x][p4y] != -1:
                            if self.turn == 0:
                                self.checkGreenSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.greenScore += (max(deltax, deltay)+1)**2
                            else:
                                self.checkYellowSquares.append([r, c, row, col, p3x, p3y, p4x, p4y])
                                self.yellowScore += (max(deltax, deltay)+1)**2
                            print("Case 8")

                #PLayer Scores
                if len(self.checkGreenSquares) - green_length >= 2:
                    self.greenmultiplier = len(self.checkGreenSquares) - green_length
                    initialScore1 += (self.greenScore - initialScore1)* self.greenmultiplier
                    self.greenScore = initialScore1
                else:
                    self.greenmultiplier = 1

                if len(self.checkYellowSquares) - yellow_length >= 2:
                    self.yellowmultiplier = len(self.checkYellowSquares) - yellow_length
                    initialScore2 += (self.yellowScore - initialScore2)* self.yellowmultiplier
                    self.yellowScore = initialScore2
                else:
                    self.yellowmultiplier = 1


        print(self.checkGreenSquares)
        print(self.checkYellowSquares)


    def mousePressEvent(self,event):
        self.__x = event.x()
        self.__y = event.y()
        #print(event.x(), event.y())
        col = (event.x() - GRID_ORIGINX)// CELL_SIZE
        row = (event.y() - GRID_ORIGINY)// CELL_SIZE
        if 0 <= row <8 and 0<= col <8:
            if self.board[row][col]== -1:
                self.board[row][col] = self.turn
                self.counter += 1
                if self.turn  == 0:
                    self.match(row, col)
                    self.turn = 1
                else:
                    self.match(row, col)
                    self.turn = 0

        print(row, col)
        self.update()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = TribeSquares()
  sys.exit(app.exec_())
