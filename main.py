import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone = pygame.image.load("Recursos/icone.png")
celta = pygame.image.load("Recursos/celta.png")
fundo = pygame.image.load("Recursos/fundo.png")
fundoStart = pygame.image.load("Recursos/fundoStart.png")
fundoDead = pygame.image.load("Recursos/fundoDead.png")

injecao = pygame.image.load("Recursos/injecao.png")
buraco = pygame.image.load('Recursos/buraco.png')
tamanho = (800, 600)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Celta Crash")
pygame.display.set_icon(icone)
buracoSound = pygame.mixer.Sound("Recursos/danger.wav")
batidaSound = pygame.mixer.Sound("Recursos/batida.wav")
fonte = pygame.font.SysFont("comicsans", 28)
fonteStart = pygame.font.SysFont("comicsans", 55)
fonteMorte = pygame.font.SysFont("arial", 120)
pygame.mixer.music.load("Recursos/Ronco.mp3")

branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)

def jogar(nome):
    pygame.mixer.Sound.play(buracoSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 700
    posicaoYPersona = 450
    movimentoXPersona = 0
    movimentoYPersona = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    posicaoXBuraco = random.randint(0, 800)
    posicaoYBuraco = -240
    velocidadeBuraco = 1
    pontos = 0
    larguraPersona = 226
    alturaPersona = 127
    larguraMissel = 50
    alturaMissel = 63
    larguraBuraco = 50
    alturaBuraco = 50
    dificuldade = 20

    # Variáveis para o círculo amarelo pulsante
    raio = 60
    pulse = 0.2
    maximo_raio = 70
    minimo_raio = 50

    # Variáveis para o círculo preto em movimento
    posicaoXCirculoPreto = random.randint(0, 800)
    posicaoYCirculoPreto = random.randint(0, 600)
    movimentoXCirculoPreto = random.choice([-3, 3])
    movimentoYCirculoPreto = random.choice([-3, 3])

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
            
        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona

        if posicaoXPersona < 0:
            posicaoXPersona = 10
        elif posicaoXPersona > 550:
            posicaoXPersona = 540
        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > 473:
            posicaoYPersona = 473

        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        tela.blit(celta, (posicaoXPersona, posicaoYPersona))

        # Atualização do círculo amarelo pulsante
        raio += pulse
        if raio >= maximo_raio or raio <= minimo_raio:
            pulse = -pulse
        pygame.draw.circle(tela, amarelo, (700, 100), raio)

        # Atualização do círculo preto em movimento
        posicaoXCirculoPreto += movimentoXCirculoPreto
        posicaoYCirculoPreto += movimentoYCirculoPreto
        if posicaoXCirculoPreto < 0 or posicaoXCirculoPreto > 800:
            movimentoXCirculoPreto = -movimentoXCirculoPreto
        if posicaoYCirculoPreto < 0 or posicaoYCirculoPreto > 600:
            movimentoYCirculoPreto = -movimentoYCirculoPreto
        pygame.draw.circle(tela, preto, (posicaoXCirculoPreto, posicaoYCirculoPreto), 10)

        posicaoYMissel += velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos += 1
            velocidadeMissel += 1
            posicaoXMissel = random.randint(0, 800)
            pygame.mixer.Sound.play(buracoSound)

        tela.blit(injecao, (posicaoXMissel, posicaoYMissel))

        posicaoYBuraco += velocidadeBuraco
        if posicaoYBuraco > 600:
            posicaoYBuraco = -240
            pontos += 1
            velocidadeBuraco += 2
            posicaoXBuraco = random.randint(0, 800)

        tela.blit(buraco, (posicaoXBuraco, posicaoYBuraco))

        texto = fonte.render(nome + "- Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (10, 10))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguraMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))
        pixelsBuracoX = list(range(posicaoXBuraco, posicaoXBuraco + larguraBuraco))
        pixelsBuracoY = list(range(posicaoYBuraco, posicaoYBuraco + alturaBuraco))

        if len(list(set(pixelsMisselY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list(set(pixelsMisselX).intersection(set(pixelsPersonaX)))) > dificuldade:
                dead(nome, pontos)
        if len(list(set(pixelsBuracoY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list(set(pixelsBuracoX).intersection(set(pixelsPersonaX)))) > dificuldade:
                dead(nome, pontos)

        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(batidaSound)

    jogadas = {}
    try:
        arquivo = open("historico.txt", "r", encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt", "w", encoding="utf-8")
        arquivo.close()

    jogadas[nome] = pontos
    arquivo = open("historico.txt", "w", encoding="utf-8")
    arquivo.write(str(jogadas))
    arquivo.close()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400, 482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60, 482))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt", "r", encoding="utf-8")
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass

    nomes = sorted(estrelas, key=estrelas.get, reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330, 482))

        posicaoY = 50
        for key, nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - " + str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300, posicaoY))
            posicaoY += 30

        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("Iron Man", "Nome Completo:")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        buttonRanking = pygame.draw.rect(tela, preto, (35, 50, 200, 50), 0, 30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90, 50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330, 482))

        pygame.display.update()
        relogio.tick(60)


start()
