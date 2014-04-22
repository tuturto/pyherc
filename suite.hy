(import [subprocess [call]])
(import [os [chdir listdir]])
(import [shutil [rmtree]])
(import [platform [system]])
(import xunit)

(call ["nosetests" "--with-xunit" "--doctest-tests" "--with-coverage"
		   "--cover-html" "--traverse-namespace"
		   "--cover-html-dir=./doc/cover" "--cover-package=pyherc"
		   "--cover-package=herculeum"])

(chdir "doc/api")
(if (in "Windows" (system))
  (call ["make.bat" "doctest"])
  (call ["make" "doctest"]))
(chdir "../../")

(call ["behave" "src/pyherc/test/bdd/features/" "--no-source" "--no-logcapture"
		"--no-color" "--outfile=doc/behave_report.txt"])

(.main xunit)
