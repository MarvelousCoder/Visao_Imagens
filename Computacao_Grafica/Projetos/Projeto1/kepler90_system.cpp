#include <GL/glut.h>
#include <math.h>
#include <GL/glu.h>
#include <GL/glext.h>
#include <GL/gl.h>
#define PI 3.1415926535897932384626433832795

static int mercuryRadius = 200;
static int venusRadius = mercuryRadius + 150;
static int earthRadius = venusRadius + 150;
static int marsRadius = earthRadius + 150;
static int jupiterRadius = marsRadius + 200;
static int saturnRadius = jupiterRadius + 200;
static int uranusRadius = saturnRadius + 150;
static int neptuneRadius = uranusRadius + 150;

static int kepler90bRadius = 1.31 * earthRadius;
static int kepler90cRadius = 1.19 * earthRadius;
static int kepler90iRadius = 1.32 * earthRadius;
static int kepler90dRadius = 0.256 * jupiterRadius;
static int kepler90eRadius = 0.237 * jupiterRadius;
static int kepler90fRadius = 0.257 * jupiterRadius;
static int kepler90gRadius = 0.723 * jupiterRadius;
static int kepler90hRadius = 1.008 * jupiterRadius;

static float kepler90b = 360.0 / 7.0;
static float kepler90c = 360.0 / 8.7;
static float kepler90i = 360.0 / 14.4;
static float kepler90d = 360.0 / 59.7;
static float kepler90e = 360.0 / 91.9;
static float kepler90f = 360.0 / 124.9;
static float kepler90g = 360.0 / 210.6;
static float kepler90h = 360.0 / 331.6;

static float kepler90bAngle = 0.0f;
static float kepler90cAngle = 0.0f;
static float kepler90iAngle = 0.0f;
static float kepler90dAngle = 0.0f;
static float kepler90eAngle = 0.0f;
static float kepler90fAngle = 0.0f;
static float kepler90gAngle = 0.0f;
static float kepler90hAngle = 0.0f;


float eyeX = 0.0f;
float eyeY = 800.0f;
float eyeZ = 1700.0f;


GLfloat mat_ambient[] = {0.7, 0.7, 0.7, 1.0};
GLfloat mat_specular[] = {0.0, 0.0, 0.0, 0.0};
GLfloat mat_shininess[] = {50.0};
GLfloat light_position[] = {1.0, 1.0, 1.0, 1.0};
GLfloat model_ambient[] = {1.0, 1.0, 1.0, 1.0};


void setupMaterials()
{
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient);
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);
    glLightfv(GL_LIGHT0, GL_POSITION, light_position);
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, model_ambient);
}

void changeColour(GLfloat r, GLfloat g, GLfloat b, GLfloat A) {
    model_ambient[0] = r;
    model_ambient[1] = g;
    model_ambient[2] = b;
    model_ambient[3] = A;
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, model_ambient);
}


void changeSize(int w, int h)
{
    if(h == 0) h = 1;
    float ratio = 1.0 * w / h;

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glViewport(0, 0, w, h);
    gluPerspective(45, ratio, 1, 5000);

    glMatrixMode(GL_MODELVIEW);
}

float angle = 0.0f;
float j = 0.0f;


void renderScene(void) {

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glLoadIdentity();

	gluLookAt(  0.0f, eyeY, eyeZ,
				0.0f, 0.0f,  0.0f,
				0.0f, 1.0f,  0.0f);

    changeColour(1.0, 1.0, 1.0, 1.0);

    //*///--------------------------------- Paths ------------------------------------------///
    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / kepler90bRadius) //<-- Change this Value
 					glVertex3f(cos(i) * kepler90bRadius, 1.0, sin(i) * kepler90bRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / kepler90cRadius) //<-- Change this Value
 					glVertex3f(cos(i) * kepler90cRadius, 1.0, sin(i) * kepler90cRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / kepler90iRadius) //<-- Change this Value
 					glVertex3f(cos(i) * kepler90iRadius, 1.0, sin(i) * kepler90iRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / kepler90dRadius) //<-- Change this Value
 					glVertex3f(cos(i) * kepler90dRadius, 1.0, sin(i) * kepler90dRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / kepler90eRadius) //<-- Change this Value
 					glVertex3f(cos(i) * kepler90eRadius, 1.0, sin(i) * kepler90eRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / kepler90fRadius) //<-- Change this Value
 					glVertex3f(cos(i) * kepler90fRadius, 1.0, sin(i) * kepler90fRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / kepler90gRadius) //<-- Change this Value
 					glVertex3f(cos(i) * kepler90gRadius, 1.0, sin(i) * kepler90gRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / kepler90hRadius) //<-- Change this Value
 					glVertex3f(cos(i) * kepler90hRadius, 1.0, sin(i) * kepler90hRadius);
    glEnd();

    ///----------------------------------------------------------------------------------///*/

	// Kepler90
	glPushMatrix();
	glRotatef(angle, 0.0f, 1.0f, 0.0f);
	changeColour(1.0, 1.0, 0.0, 0.0);
	GLUquadric *Kepler90;
    Kepler90 = gluNewQuadric();
    gluSphere(Kepler90, 100, 100, 100);
    //glutWireSphere(200, 30, 30);
    glPopMatrix();

	// Kepler-90b
	glPushMatrix();
    glRotatef(kepler90bAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(kepler90bRadius, 0.0, 0.0);
	changeColour(66/255.0, 61/255.0, 57/255.0, 0.0);
	GLUquadric *Kepler90b;
    Kepler90b = gluNewQuadric();
    gluSphere(Kepler90b, 10, 100, 100);
	glPopMatrix();


	// Kepler-90c
	glPushMatrix();
    glRotatef(kepler90cAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(kepler90cRadius,0.0, 0.0);
	changeColour(140.0/255.0, 70.0/255.0, 0.0, 0.0);
	GLUquadric *Kepler90c;
    Kepler90c = gluNewQuadric();
    gluSphere(Kepler90c, 25.8, 100, 100);
	glPopMatrix();

	// Kepler90i
	glPushMatrix();
    glRotatef(kepler90iAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(kepler90iRadius,0.0, 0.0);
	changeColour(0.0, 0.007, 0.686, 0.0);
	GLUquadric *Kepler90i;
    Kepler90i = gluNewQuadric();
    gluSphere(Kepler90i, 20.6, 100, 100);
    glPopMatrix();

	// Kepler90d
	glPushMatrix();
    glRotatef(kepler90dAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(kepler90dRadius,0.0, 0.0);
	changeColour(170/255.0, 60/255.0, 5/255.0, 0.0);
	GLUquadric *Kepler90d;
    Kepler90d = gluNewQuadric();
    gluSphere(Kepler90d, 18.4, 100, 100);
	glPopMatrix();

	// Kepler90e
	glPushMatrix();
    glRotatef(kepler90eAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(kepler90eRadius,0.0, 0.0);
	glRotatef(angle+angle*4, 0.0f, 1.0f, 0.0f); /// Rotate in Own axis
	changeColour(53/255.0, 107/255.0, 112/255.0, 0.0);
	GLUquadric *Kepler90e;
    Kepler90e = gluNewQuadric();
    gluSphere(Kepler90e,64.5,100,100);
    //glutWireSphere(64.5, 30, 30);
	glPopMatrix();


	// kepler90f
	glPushMatrix();
    glRotatef(kepler90fAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(kepler90fRadius,0.0, 0.0);
	glRotatef(angle+angle*4, 0.0f, 1.0f, 0.0f); /// Rotate in Own axis
	changeColour(165/255.0, 138/255.0, 38/255.0, 0.0);
	GLUquadric *Kepler90f;
    Kepler90f = gluNewQuadric();
    gluSphere(Kepler90f,54,100,100);
	glPopMatrix();

	// kepler90g
	glPushMatrix();
    glRotatef(kepler90gAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(kepler90gRadius,0.0, 0.0);
	changeColour(53/255.0, 198/255.0, 198/255.0, 0.0);
	GLUquadric *Kepler90g;
    Kepler90g = gluNewQuadric();
    gluSphere(Kepler90g,22.5,100,100);
    glPopMatrix();

	// kepler90h
	glPushMatrix();
    glRotatef(kepler90hAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(kepler90hRadius,0.0, 0.0);
	changeColour(5/255.0, 5/255.0, 186/255.0, 0.0);
	GLUquadric *Kepler90h;
    Kepler90h = gluNewQuadric();
    gluSphere(Kepler90h,24,100,100);
    glPopMatrix();

	angle += 0.2f;
	kepler90bAngle += kepler90b / 10;
	kepler90cAngle += kepler90c / 10;
	kepler90iAngle += kepler90i / 10;
	kepler90dAngle += kepler90d / 10;
	kepler90eAngle += kepler90e / 2;
	kepler90fAngle += kepler90f / 2;
	kepler90gAngle += kepler90g * 10;
	kepler90hAngle += kepler90h * 10;

	//if(angle == 360) angle = 0;
	glutSwapBuffers();
}


void mouse(int button, int state, int x, int y)
{
    switch (button) {
        case GLUT_LEFT_BUTTON:
            if (state == GLUT_DOWN)
            glutIdleFunc(renderScene);
            break;
        case GLUT_RIGHT_BUTTON:
            if (state == GLUT_DOWN)
            glutIdleFunc(NULL);
            break;
    }
}

void keyboard(unsigned char key, int xx, int yy) {
    switch (key) {
        case 27:
            exit(0);
            break;
    }
}

void keyboardSpecial(int key, int xx, int yy)
{
    switch (key) {
    case GLUT_KEY_UP:
        eyeY -= 10.0f;
        eyeZ -= 10.0f;
        break;
    case GLUT_KEY_DOWN:
        eyeY += 10.0f;
        eyeZ += 10.0f;
        break;
    }
}


void init(void) {
    glClearColor(0.0, 0.0, 0.0, 1.0);
    setupMaterials();
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_CULL_FACE);
    glFrontFace(GL_CCW);
    glShadeModel(GL_SMOOTH);
}

int main(int argc, char * argv[]) {

    // init GLUT and create window
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowPosition(100, 100);
    glutInitWindowSize(1000, 500);
    //glOrtho(-1000, 1000, -1000, 1000, -1000, 1000);
    glutCreateWindow("Kepler System");
    init();

    // register callbacks
    glutDisplayFunc(renderScene);
    glutReshapeFunc(changeSize);
    glutMouseFunc(mouse);
    glutKeyboardFunc(keyboard);
    glutSpecialFunc(keyboardSpecial);

    // enter GLUT event processing cycle
    glutMainLoop();
    return 0;
}
