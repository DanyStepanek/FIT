PROJ=proj5
PACK=xstepa61-fit
IMAGES_DIRECTORY=./img
PACKAGES=algorithm2e.sty

.PHONY: pdflatex pack clean

pdflatex: $(PROJ).tex
	pdflatex $^
	pdflatex $^

pack:	$(PACK).tar.gz

$(PACK).tar.gz: $(PROJ).tex $(IMAGES_DIRECTORY) $(PACKAGES)
	tar -czf $@ $^ Makefile

clean:
	rm -f $(PROJ).aux $(PROJ).log	$(PROJ).dvi  $(PROJ).ps	$(PROJ).nav	$(PROJ).out	$(PROJ).snm	$(PROJ).toc
