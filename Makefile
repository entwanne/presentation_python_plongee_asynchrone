PRES = pres.ipynb
NOTES = notes.pdf
SRC = $(shell find src -name "*.md" | sort -n)

GEN = $(PRES) $(NOTES)

$(PRES):	$(SRC)
		lucina -o $@ $^ --no-autolaunch

$(NOTES):	notes.md
		pandoc -V geometry:margin=0.3in $^ -o $@


pres:		$(PRES)

notes:		$(NOTES)

clean:
		rm -f $(GEN)

re:		clean $(GEN)

.PHONY:		pres notes clean re
