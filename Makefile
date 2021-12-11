clean:
	find . -name "*.pyc" -exec rm -f {} \;
	rm -rf target
	rm -rf __pycache__

package: clean
	mkdir target
	cp keyword_perf/main.py target/
	zip -r -X target/keyword_perf.zip keyword_perf

run-local: package
	spark-submit --py-files target/keyword_perf.zip target/main.py data.tsv

ubuntu-deploy: package
	sudo apt-get update; sudo apt-get -y install make
	aws s3 sync ./target/ s3://jays-apps/payloads/search-keyword-performance/
