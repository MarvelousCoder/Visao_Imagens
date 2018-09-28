all:
	g++ -std=c++11 pd3.cpp `pkg-config --libs --cflags opencv` -I/usr/local/include -L/usr/local/lib -o pd3
	./pd3
r:
	g++ -std=c++11 disparity_filtering.cpp `pkg-config --libs --cflags opencv` -I/usr/local/include -L/usr/local/lib -o teste
	./teste data/babyL.png data/babyR.png sgbm wls_conf 1.0 160 7 8000.0 1.5