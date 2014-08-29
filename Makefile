
clean:
	rm -rf input.txt jsoncatalog.txt bookworm
	mysql << echo "DROP DATABASE simpsons"

input.txt:
	python parseSRT.py data/*.srt

bookworm:
	git clone git@github.com:bmschmidt/Presidio bookworm
	cd bookworm; git checkout master
	mkdir -p bookworm/files
	mkdir -p bookworm/files/metadata
	mkdir -p bookworm/files/texts

bookworm/files/texts/input.txt: input.txt
	cp $< $@

bookworm/files/metadata/field_descriptions.json: field_descriptions.json
	cp $< $@

bookworm/files/metadata/jsoncatalog.txt: jsoncatalog.txt
	cp $< $@

bookwormdatabase: bookworm bookworm/files/texts/input.txt bookworm/files/metadata/jsoncatalog.txt bookworm/files/metadata/field_descriptions.json
	cd bookworm; git checkout master
	cd bookworm; make;

