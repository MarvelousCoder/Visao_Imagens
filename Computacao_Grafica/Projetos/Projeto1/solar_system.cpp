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

static float mercury = 360.0 / 87.97;
static float venus = 360.0 / 224.70;
static float earth = 360.0 / 365.26;
static float mars = 360.0 / 686.98;
static float jupiter = 360.0 / 4332.82;
static float saturn = 360.0 / 10755.7;
static float uranus = 360.0 / 306871.5;
static float neptune = 360.0 / 601900.3;

static float mercuryAngle = 0.0f;
static float venusAngle = 0.0f;
static float earthAngle = 0.0f;
static float marsAngle = 0.0f;
static float jupiterAngle = 0.0f;
static float saturnAngle = 0.0f;
static float uranusAngle = 0.0f;
static float neptuneAngle = 0.0f;


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

	gluLookAt(	0.0f, eyeY, eyeZ,
				0.0f, 0.0f,  0.0f,
				0.0f, 1.0f,  0.0f);

    changeColour(1.0, 1.0, 1.0, 1.0);

    //*///--------------------------------- Paths ------------------------------------------///
    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / mercuryRadius) //<-- Change this Value
 					glVertex3f(cos(i) * mercuryRadius, 1.0, sin(i) * mercuryRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / venusRadius) //<-- Change this Value
 					glVertex3f(cos(i) * venusRadius, 1.0, sin(i) * venusRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / earthRadius) //<-- Change this Value
 					glVertex3f(cos(i) * earthRadius, 1.0, sin(i) * earthRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / marsRadius) //<-- Change this Value
 					glVertex3f(cos(i) * marsRadius, 1.0, sin(i) * marsRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / jupiterRadius) //<-- Change this Value
 					glVertex3f(cos(i) * jupiterRadius, 1.0, sin(i) * jupiterRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / saturnRadius) //<-- Change this Value
 					glVertex3f(cos(i) * saturnRadius, 1.0, sin(i) * saturnRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / uranusRadius) //<-- Change this Value
 					glVertex3f(cos(i) * uranusRadius, 1.0, sin(i) * uranusRadius);
    glEnd();

    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / neptuneRadius) //<-- Change this Value
 					glVertex3f(cos(i) * neptuneRadius, 1.0, sin(i) * neptuneRadius);
    glEnd();

    ///----------------------------------------------------------------------------------///*/



	// The Sun
	glPushMatrix();
	glRotatef(angle, 0.0f, 1.0f, 0.0f);
	changeColour(1.0, 1.0, 0.0, 0.0);
	GLUquadric *sun;
    sun = gluNewQuadric();
    gluSphere(sun,100,100,100);
    //glutWireSphere(200, 30, 30);
    glPopMatrix();

	// Mercury
	glPushMatrix();
    glRotatef(mercuryAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(mercuryRadius, 0.0, 0.0);
	changeColour(66/255.0, 61/255.0, 57/255.0, 0.0);
	GLUquadric *Mercury;
    Mercury = gluNewQuadric();
    gluSphere(Mercury,10,100,100);
	glPopMatrix();


	// Venus
	glPushMatrix();
    glRotatef(venusAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(venusRadius,0.0, 0.0);
	changeColour(140.0/255.0, 70.0/255.0, 0.0, 0.0);
	GLUquadric *Venus;
    Venus = gluNewQuadric();
    gluSphere(Venus,25.8,100,100);
	glPopMatrix();

	// Earth
	glPushMatrix();
    glRotatef(earthAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(earthRadius,0.0, 0.0);
	changeColour(0.0, 0.007, 0.686, 0.0);
	GLUquadric *Earth;
    Earth = gluNewQuadric();
    gluSphere(Earth,20.6,100,100);
    //glPopMatrix();

    //Moon
    glRotatef(5*earthAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(50,0.0, 0.0);
	changeColour(0.7, 0.7, 0.7, 0.0);
	GLUquadric *Moon;
    Moon = gluNewQuadric();
    gluSphere(Moon,7,100,100);
    glPopMatrix();

    //*
    glPushMatrix();
    glRotatef(earthAngle, 0.0f, 1.0f, 0.0f);
    glTranslatef(earthRadius,0.0, 0.0);
    changeColour(1.0, 1.0, 1.0, 1.0);
    glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / 1000) glVertex3f(cos(i) * 50, 0.0,  sin(i) * 50);
    glEnd();
	glPopMatrix();
	//*/

	// Mars
	glPushMatrix();
    glRotatef(marsAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(marsRadius,0.0, 0.0);
	changeColour(170/255.0, 60/255.0, 5/255.0, 0.0);
	GLUquadric *Mars;
    Mars = gluNewQuadric();
    gluSphere(Mars,18.4,100,100);
	glPopMatrix();

	// Jupitar
	glPushMatrix();
    glRotatef(jupiterAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(jupiterRadius,0.0, 0.0);
	glRotatef(angle+angle*4, 0.0f, 1.0f, 0.0f); /// Rotate in Own axis
	changeColour(53/255.0, 107/255.0, 112/255.0, 0.0);
	GLUquadric *Jupitar;
    Jupitar = gluNewQuadric();
    gluSphere(Jupitar,64.5,100,100);
    //glutWireSphere(64.5, 30, 30);
	glPopMatrix();


	// Saturn
	glPushMatrix();
    glRotatef(saturnAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(saturnRadius,0.0, 0.0);
	glRotatef(angle+angle*4, 0.0f, 1.0f, 0.0f); /// Rotate in Own axis
	changeColour(165/255.0, 138/255.0, 38/255.0, 0.0);
	GLUquadric *Saturn;
    Saturn = gluNewQuadric();
    gluSphere(Saturn,54,100,100);
	glPopMatrix();

	glPushMatrix();
	glRotatef(saturnAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(saturnRadius,0.0, 0.0);
	glRotatef(80.0f, 1.0f, 0.0f, 0.0f); /// Rotate the circles
	changeColour(163/255.0, 149/255.0, 79/255.0, 0.0);
	glBegin(GL_POINTS);
    for(double i = 0; i < 2 * PI; i += PI / 1000) glVertex3f(cos(i) * 70,  sin(i) * 70, 0.0);
    for(double i = 0; i < 2 * PI; i += PI / 1000) glVertex3f(cos(i) * 75,  sin(i) * 75, 0.0);
    for(double i = 0; i < 2 * PI; i += PI / 1000) glVertex3f(cos(i) * 80,  sin(i) * 80, 0.0);
    for(double i = 0; i < 2 * PI; i += PI / 1000) glVertex3f(cos(i) * 85,  sin(i) * 85, 0.0);
    for(double i = 0; i < 2 * PI; i += PI / 1000) glVertex3f(cos(i) * 90,  sin(i) * 90, 0.0);
    for(double i = 0; i < 2 * PI; i += PI / 1000) glVertex3f(cos(i) * 95,  sin(i) * 95, 0.0);
    for(double i = 0; i < 2 * PI; i += PI / 1000) glVertex3f(cos(i) * 100,  sin(i) * 100, 0.0);
    glEnd();

	glPopMatrix();

	// Uranus
	glPushMatrix();
    glRotatef(uranusAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(uranusRadius,0.0, 0.0);
	changeColour(53/255.0, 198/255.0, 198/255.0, 0.0);
	GLUquadric *Uranus;
    Uranus = gluNewQuadric();
    gluSphere(Uranus,22.5,100,100);
    glPopMatrix();

	// Neptune
	glPushMatrix();
    glRotatef(neptuneAngle, 0.0f, 1.0f, 0.0f);
	glTranslatef(neptuneRadius,0.0, 0.0);
	changeColour(5/255.0, 5/255.0, 186/255.0, 0.0);
	GLUquadric *Neptune;
    Neptune = gluNewQuadric();
    gluSphere(Neptune,24,100,100);
    glPopMatrix();

	angle += 0.2f;
	mercuryAngle += mercury / 10;
	venusAngle += venus / 10;
	earthAngle += earth / 10;
	marsAngle += mars / 10;
	jupiterAngle += jupiter / 2;
	saturnAngle += saturn / 2;
	uranusAngle += uranus * 10;
	neptuneAngle += neptune * 10;

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
    glutCreateWindow("Solar System");
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
