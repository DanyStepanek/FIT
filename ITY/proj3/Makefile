PROJ=proj3
PACK=xstepa61-fit
IMAGES_DIRECTORY=./img
PACKAGES=algorithm2e.sty

.PHONY: clean pack pdflatex

$(PROJ).pdf: $(PROJ).ps
	ps2pdf -sPAPERSIZE=a4 $^

$(PROJ).ps: $(PROJ).dvi
	dvips $^

$(PROJ).dvi: $(PROJ).tex
	latex $^
	latex $^

$(PACK).tar.gz: $(PROJ).tex $(IMAGES_DIRECTORY) $(PACKAGES)
	tar -czf $@ $^ Makefile

pdflatex: $(PROJ).tex
	pdflatex $^

pack: clean $(PACK).tar.gz

clean:
	rm -f $(PROJ).aux $(PROJ).dvi $(PROJ).log $(PROJ).ps $(PROJ).synctex.gz $(PROJ).fls $(PROJ).fdb_latexmk $(wildcard $(IMAGES_DIRECTORY)/*.pdf)
