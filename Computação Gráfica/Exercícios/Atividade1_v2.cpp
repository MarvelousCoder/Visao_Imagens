#include <GL/glut.h>
#include <cmath>
#include <iostream>

void rotacao2D(GLfloat angle);
void translacao2D(GLfloat tx, GLfloat ty);
void escala2D(GLfloat x, GLfloat y);

char tecla = 'n';

GLfloat cx = (0.5f + 0.5f + 0.7f + 0.7f)/4.0;
GLfloat cy = (0.5f + 0.7f + 0.7f + 0.5f)/4.0;

void operacao(GLubyte key, GLint xMouse, GLint yMouse) 
{
    switch (key) {
        case 'r':
            tecla = 'r';
            break;
        case 's':
            tecla = 's';
            break;
        case 't':
            tecla = 't';
            break;
        default:
            tecla = 'n';
            break;
    }
}

void executaOperacao(GLint specialKey, GLint xMouse, GLint yMouse) 
{   
    switch (specialKey)
    {
        case GLUT_KEY_UP:
            if(tecla == 'r') rotacao2D(0.9f);
            else if (tecla == 's') escala2D(2.0f, 2.0f);
            else if (tecla == 't') { translacao2D(0.0f, 0.1f); cy += 0.0f; }
            break;
        case GLUT_KEY_DOWN:
            if(tecla == 'r') rotacao2D(-0.9f);
            else if (tecla == 's') escala2D(0.5f, 0.5f);
            else if (tecla == 't') { translacao2D(0.0f, -0.1f); cy -= 0.0f; }
            break;
        case GLUT_KEY_LEFT:
            if (tecla == 't') { translacao2D(-0.1f, 0.0f); cx -= 0.0f; } 
            break;
        case GLUT_KEY_RIGHT:
            if (tecla == 't') { translacao2D(0.1f, 0.0f); cx += 0.0f; }
            break;
        default:
            break;
    }
}

void rotacao2D(GLfloat angle) 
{
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glPopMatrix();
    glTranslatef(cx, cy, 0.0f);

    glRotatef(angle, 0.0f, 0.0f, 1.0f);
    glTranslatef(-cx, -cy, 0.0f);
    glPushMatrix();
}

void translacao2D(GLfloat tx, GLfloat ty) {
    /* Habilita a matriz de transformações geométricas */
    glMatrixMode(GL_MODELVIEW);

    /* Reseta a matriz de modelo para transformações geométricas, colocando-a como
    Identidade */
    glLoadIdentity();

    /* Recupera o estado da Matriz na pilha antes da translação */
    /* Pode ser usado para mover quadrados, por exemplo */
    glPopMatrix();

    glTranslatef(tx, ty, 0.0f);
    glPushMatrix();
    /* Salva o estado da Matriz na pilha antes da translação */
}

void escala2D(GLfloat x, GLfloat y) 
{
    glMatrixMode(GL_MODELVIEW);

    glLoadIdentity();
    glPopMatrix();
    glTranslatef(cx, cy, 0.0f);
    glScalef(x, y, 0.0f);
    glTranslatef(-cx, -cy, 0.0f);

    glPushMatrix();
}

void drawRectangle() 
{
    glColor3f(0.0f, 0.0f, 1.0f);
    glBegin(GL_QUADS);
        glVertex2f(0.5f, 0.5f);
        glVertex2f(0.5f, 0.7f);
        glVertex2f(0.7f, 0.7f);
        glVertex2f(0.7f, 0.5f);
    glEnd();
}

void criaCena() 
{
    /* Limpa o buffer e coloca a cor padrão de fundo */
    glClear(GL_COLOR_BUFFER_BIT);

    drawRectangle();
    glFlush();
    glutPostRedisplay();
}


int main(int argc, char** argv)
{
    glutInit(&argc, argv);
    /* Iniciar a GLUT para que recursos computacionais sejam disponibilizados para este programa */
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);

    glutInitWindowSize(600, 600);

    /* Coordenadas da tela inicial da janela do OpenGL */
    glutInitWindowPosition(50, 50);

    /* Cria a janela */
    glutCreateWindow("Atividade pratica 1");

    /* Função que cria processo de renderização */
    // Objeto quadrado;
    glutDisplayFunc(criaCena);

    /* Habilitar o teclado usando recursos da GLUT, chama o método keyboard_special */
    glutKeyboardFunc(operacao);
    glutSpecialFunc(executaOperacao);


    /* Coloca esse programa OpenGL em loop infinito */
    glutMainLoop();
    return 0;
}