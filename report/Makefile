LATEX=pdflatex
BIB=biber
PDFS=$(patsubst %.tex, %.pdf, $(wildcard *.tex))
all: $(PDFS) clean

%.pdf : %.tex
	$(LATEX) $^
	$(LATEX) $^
	$(BIB) $(basename $^)
	$(LATEX) $^
	$(LATEX) $^
	
clean:
	@rm -rf *.aux *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log *.run.xml *.synctex.gz *.dvi
remove: clean
	@rm -rf *.pdf
