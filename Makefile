OUTPUT_BASENAME ?= all_notes
OUTPUT_HTML = $(OUTPUT_BASENAME).html
OUTPUT_PDF = $(OUTPUT_BASENAME).pdf
NOTES_TODAY = $(shell ls markdown_notes/notes_*.md | tail -n1)
NOTES_TODAY_PDF = notes_today.pdf

all: pdf

pdf:
	./convert.py markdown_notes/notes_*.md \
	    && asciidoctor-pdf merged.adoc -o $(OUTPUT_PDF) \
	    && pdfnup --nup 2x1 --suffix 2x1 $(OUTPUT_PDF) \
	    && rm merged.adoc
	@echo "Output written to file '$(OUTPUT_PDF)'."

# Re-create the file notes_today.pdf every second
watch:
	while true; do \
	    make notes-today > /dev/null; \
	    sleep 1; \
	done

# Alias for convenience
notes-today: $(NOTES_TODAY_PDF)

$(NOTES_TODAY_PDF): $(NOTES_TODAY)
	./convert.py $(NOTES_TODAY) \
		&& asciidoctor-pdf merged.adoc -o $(NOTES_TODAY_PDF) \
		&& rm merged.adoc

html:
	pandoc markdown_notes/notes*.md -f markdown -t html -s -o $(OUTPUT_HTML)
	@echo "Output written to file '$(OUTPUT_HTML)'."

clean:
	rm -f $(OUTPUT_HTML) $(OUTPUT_PDF) $(NOTES_TODAY_PDF)

.PHONY: all pdf html watch notes-today clean
