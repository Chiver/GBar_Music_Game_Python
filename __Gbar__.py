import game_final_version1 as gfv
import pygame, math, random, time
import audio_processing_version2 as ad

def main(g):
    g.showStartScreen()
    while g.running:
        pygame.time.delay(50)
        if g.selectionMode:
            g.showSelectionMode()
            g.playMusic()
        g.checkGameOver()
        g.generateRect()
        g.eventHandler()
        g.updateGame()
        g.redrawAll()
    g.drawGameOver()

if __name__ == '__main__':
    g = gfv.RunGame(500, 500, time)
    main(g)
    pygame.quit()
