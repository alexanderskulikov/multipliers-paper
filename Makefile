all: 
	latexmk -pdf multipliers
	open multipliers.pdf

clean:
	latexmk -pdf -c
