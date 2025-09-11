all: 
	latexmk -pdf multipliers_lipics
	open multipliers_lipics.pdf

clean:
	latexmk -pdf -c
