PROJ=proj4
PACK=xstepa61-fit
INCLUDE=czechiso.bst
.PHONY: pdflatex pack clean

$(PROJ).pdf: $(PROJ).ps
	ps2pdf $^


$(PROJ).ps: $(PROJ).dvi
	dvips $^


$(PROJ).dvi: $(PROJ).tex
	latex $^
	latex $^


pdflatex: $(PROJ).tex
	pdflatex $^
	pdflatex $^


pack: clean $(PACK).tar.gz

$(PACK).tar.gz: $(PROJ).tex $(IMAGES_DIRECTORY)
	tar -czf $@ $^ Makefile


clean:
	rm -f $(PROJ).aux $(PROJ).dvi $(PROJ).log $(PROJ).ps $(PROJ).synctex.gz $(PROJ).fls $(PROJ).fdb_latexmk $(PROJ).bbl $(PROJ).blg
