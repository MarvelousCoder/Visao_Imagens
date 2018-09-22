#include <GL/glut.h>
#include <cmath>
#include <iostream>

GLsizei winWidth = 600, winHeight = 600;

/* Set range for world coordinates. */
GLfloat xwcMin = 0.0, xwcMax = 225.0;
GLfloat ywcMin = 0.0, ywcMax = 225.0;

typedef GLfloat Matrix3x3 [3][3];
Matrix3x3 matComposite;

char tecla = 'n';
char arrow = 'n';
GLdouble theta = 1.0;
GLfloat g_tx = 0.0, g_ty = 0.0;
GLfloat g_sx = 1.0, g_sy = 1.0;


class wcPt2D {
    public:
    GLfloat x, y;
};

void init (void)
{
    /* Set color of display window to white. */
    glClearColor (1.0, 1.0, 1.0, 0.0);
}

/* Construct the 3 x 3 identity matrix. */
void matrix3x3SetIdentity (Matrix3x3 matIdent3x3)
{
    GLint row, col;
    for (row = 0; row < 3; row++)
        for (col = 0; col < 3; col++)
            matIdent3x3 [row][col] = (row == col);
}

/* Premultiply matrix m1 times matrix m2, store result in m2. */
void matrix3x3PreMultiply (Matrix3x3 m1, Matrix3x3 m2)
{
    GLint row, col;
    Matrix3x3 matTemp;
    for (row = 0; row < 3; row++)
        for (col = 0; col < 3 ; col++)
        matTemp [row][col] = m1 [row][0] * m2 [0][col] + m1 [row][1] *
                                m2 [1][col] + m1 [row][2] * m2 [2][col];
    for (row = 0; row < 3; row++)
        for (col = 0; col < 3; col++)
            m2 [row][col] = matTemp [row][col];
}

void translate2D (GLfloat tx, GLfloat ty)
{
    Matrix3x3 matTransl;
    /* Initialize translation matrix to identity. */
    matrix3x3SetIdentity (matTransl);
    if(arrow == 'u') g_ty = 5.0;
    else if (arrow == 'd') g_ty = -5.0;
    else if (arrow = 'l') g_tx = -5.0;
    else if (arrow = 'r') g_tx = 5.0;
    matTransl [0][2] = g_tx;
    matTransl [1][2] = g_ty;

    /* Concatenate matTransl with the composite matrix. */
    matrix3x3PreMultiply (matTransl, matComposite);
}

void rotate2D (wcPt2D pivotPt, GLfloat theta)
{
    Matrix3x3 matRot;
    /* Initialize rotation matrix to identity. */
    matrix3x3SetIdentity (matRot);

    matRot [0][0] = cos (theta);
    matRot [0][1] = -sin (theta);
    matRot [0][2] = pivotPt.x * (1 - cos (theta)) + pivotPt.x * sin(theta);

    matRot [1][0] = sin (theta);
    matRot [1][1] = cos (theta);
    matRot [1][2] = pivotPt.y * (1 - cos (theta)) - pivotPt.x * sin(theta);

    /* Concatenate matRot with the composite matrix. */
    if(arrow == 'u') matrix3x3PreMultiply (matRot, matComposite);
    else if (arrow == 'd') {
        matRot [0][1] = sin(theta);
        matRot [0][2] = pivotPt.x * (1 - cos (theta)) - pivotPt.x * sin(theta);
        matRot [1][0] = -sin (theta);
        matRot [1][2] = pivotPt.y * (1 - cos (theta)) + pivotPt.x * sin(theta);
        matrix3x3PreMultiply (matRot, matComposite);
    }
}

void scale2D (GLfloat sx, GLfloat sy, wcPt2D fixedPt) 
{
    Matrix3x3 matScale;

    matrix3x3SetIdentity(matScale);
    if(arrow == 'u') g_sx = g_sy = 2.0;
    else if (arrow = 'd') g_sx = g_sy = 0.5;
    matScale [0][0] = g_sx;
    matScale [0][2] = (1 - g_sx) * fixedPt.x;
    matScale [1][1] = g_sy;
    matScale [1][2] = (1 - g_sy) * fixedPt.y;

    /* Concatenate matRot with the composite matrix. */
    matrix3x3PreMultiply (matScale, matComposite);
}

/* Using the composite matrix, calculate transformed coordinates. */
void transformVerts2D (GLint nVerts, wcPt2D * verts)
{
    GLint k;
    GLfloat temp;
    for (k = 0; k < nVerts; k++) {
        temp = matComposite [0][0] * verts [k].x + matComposite [0][1] *
                verts [k].y + matComposite [0][2];
        verts [k].y = matComposite [1][0] * verts [k].x + matComposite [1][1] *
                        verts [k].y + matComposite [1][2];
        verts [k].x = temp;
    }
}

void triangle (wcPt2D *verts)
{
    GLint k;

    glBegin (GL_TRIANGLES);
        for (k = 0; k < 3; k++)
            glVertex2f (verts [k].x, verts [k].y);
    glEnd ( ); 
}

void criaCena(void) 
{
    GLint nVerts = 3;
    wcPt2D verts [3] = { {30.0, 5.0}, {130.0, 5.0}, {80.0, 80.0} }; // Posição inicial do triângulo
    wcPt2D centroidPt;
    wcPt2D pivPt, fixedPt; // Parâmetros da transf. geométrica

    GLint k, xSum = 0, ySum = 0;
    for (k = 0; k < nVerts; k++) {
        xSum += verts [k].x;
        ySum += verts [k].y;
    }
    centroidPt.x = GLfloat (xSum) / GLfloat (nVerts);
    centroidPt.y = GLfloat (ySum) / GLfloat (nVerts);

    /* Set geometric transformation parameters. */

    pivPt = centroidPt;
    fixedPt = centroidPt;

    glClear (GL_COLOR_BUFFER_BIT); // Clear display window.

    // glColor3f (0.0, 0.0, 1.0);
    // triangle (verts); // Display blue triangle

    /* Initialize composite matrix to identity. */
    matrix3x3SetIdentity (matComposite);

    /* Construct composite matrix for transformation sequence. */
    
    switch (tecla)
    {
        case 'r':
            rotate2D (pivPt, theta);    
            break;
        case 's':
            scale2D (g_sx, g_sy, fixedPt);
            break;
        case 't':
            translate2D (g_tx, g_ty);
            break;
        default:
            break;
    }

    /* Apply composite matrix to triangle vertices. */
    transformVerts2D (nVerts, verts);

    glColor3f (0.0, 0.0, 1.0); // Set color for transformed triangle.
    triangle (verts); // Display red triangle.

    glFlush ( );
    glutPostRedisplay();
}

void winReshape (GLint newWidth, GLint newHeight)
{
    glMatrixMode (GL_PROJECTION);
    glLoadIdentity ( );
    gluOrtho2D (xwcMin, xwcMax, ywcMin, ywcMax);

    glClear (GL_COLOR_BUFFER_BIT);
}

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
            arrow = 'u';
            break;
        case GLUT_KEY_DOWN:
            arrow = 'd';
            break;
        case GLUT_KEY_LEFT:
            arrow = 'l';
            break;
        case GLUT_KEY_RIGHT:
            arrow = 'r';
            break;
        default:
            arrow = 'n';
            break;
    }
    /* redesenha a tela */
    // glutDisplayFunc(criaCena);
    // glutPostRedisplay();
}

int main(int argc, char** argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);

    glutInitWindowPosition(50, 50);
    glutInitWindowSize(winWidth, winHeight);
    glutCreateWindow("Atividade pratica 1");

    init ( );
    glutDisplayFunc (criaCena);
    glutReshapeFunc (winReshape);

    
    glutKeyboardFunc(operacao);
    glutSpecialFunc(executaOperacao);

    glutMainLoop();
    return 0;
}