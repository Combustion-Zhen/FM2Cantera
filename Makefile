all: FM2Cantera.C
	g++ -std=c++11 -o FM2Cantera FM2Cantera.C
clean:
	rm FM2Cantera
