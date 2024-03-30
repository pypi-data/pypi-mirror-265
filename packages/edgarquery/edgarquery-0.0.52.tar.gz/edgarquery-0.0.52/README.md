# EDGARquery

**Table of Contents**

- [Installation](#installation)
```console
pip install edgarquery
```

- [License](#license)
`edgarquery` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

-[Usage]

## edgarquery

## required environmental variable<br/>
EQEMAIL - required by the SEC to download some of the files with curl.<br/>
          used as the user-agent in the url request by the scripts.<br/>

These commands retrieve various data from SEC EDGAR. They use a<br/>
CIK or Central Index Key to identify entities such as companies or<br/>
insiders - company officers or large stock holders.<br/>
Use edgartickerstocsv and edgarcikperson to find CIKs by name<br/>
or ticker and then use that CIK to gather the data of interest.<br/>
To display facts for a company aggregated by the SEC, invoke<br/>
edgarcompanyfactshow.<br/>
<br/>
## edgartickerstocsv<br/>
<br/>
usage: edgartickerstocsv [-h] [--directory DIRECTORY]<br/>
<br/>
collect EDGAR companyticker json files and convert them to csv<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --directory DIRECTORY<br/>
                        where to deposit the fileѕ<br/>
<br/>
## edgarcikperson<br/>
<br/>
usage: edgarcikperson [-h] [--cikpersondb CIKPERSONDB] [--file FILE]<br/>
<br/>
extract CIK and person names from form345 zip files<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --cikpersondb CIKPERSONDB<br/>
                        full path to the sqlite3 database - default in memory<br/>
  --file FILE           where to store the output - default stdout<br/>
<br/>
## edgarcompanyconcepttocsv<br/>
usage: edgarcompanyconcepttocsv [-h] --file FILE [--directory DIRECTORY]<br/>
<br/>
Parse an SEC EDGAR companyconcepts json file after it has been altered to deal<br/>
with its multipart character and generate a csv file from its contents<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --file FILE           json file to process<br/>
  --directory DIRECTORY<br/>
                        where to deposit the fileѕ<br/>
<br/>
## edgarcompanyfactshow<br/>
<br/>
usage: edgarcompanyfactsshow [-h] --cik CIK [--directory DIRECTORY] [--show]<br/>
<br/>
parse EDGAR company facts for a cik and display them in a browser<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --cik CIK             Centralized Index Key for the company<br/>
  --directory DIRECTORY<br/>
                        where to store the html file to display<br/>
  --show                display the html in your browser<br/>
<br/>
## edgarcompanyfactstocsv<br/>
<br/>
usage: edgarcompanyfactstocsv [-h] --file FILE [--directory DIRECTORY]<br/>
<br/>
Parse an SEC EDGAR companyfacts json file after it has been altered to deal<br/>
with its multipart character and generate CSV files from its content<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --file FILE           json file to process<br/>
  --directory DIRECTORY<br/>
                        where to deposit the csv fileѕ<br/>
<br/>
## edgarcompanyfactsziptocsv<br/>
<br/>
usage: edgarcompanyfactsziptocsv [-h] --zipfile ZIPFILE [--directory DIRECTORY]<br/>
                               [--files FILES]<br/>
<br/>
Extract one or more json files from an SEC EDGAR companyfacts.zip file and<br/>
convert to CSV<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --zipfile ZIPFILE     submissions.zip file to process. Іt can be downloadæd<br/>
                        with edgarquery.query<br/>
  --directory DIRECTORY<br/>
                        where to deposit the output<br/>
  --files FILES         comma separated(no spaces) content file(s) to process<br/>
                        a subset of the files in the zip file<br/>
<br/>
## edgarquery<br/>
<br/>
usage: edgarquery  [-h] [--cik CIK] [--cy CY] [--frame FRAME] [--units UNITS]<br/>
                  [--fact FACT] [--directory DIRECTORY] [--file FILE]<br/>
                  [--companyconcept] [--companyfacts] [--xbrlframes]<br/>
                  [--companyfactsarchivezip] [--submissionszip]<br/>
                  [--financialstatementandnotesdataset]<br/>
<br/>
query SEC EDGAR site NOTE thæt EQEMAIL env variable is required and must<br/>
contain a valid User-Agent such as your email address<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --cik CIK             10-digit Central Index Key<br/>
  --cy CY               calendar year e.g. CY2023, CY2023Q1, CY2023Q4I<br/>
  --frame FRAME         reporting frame e.g us-gaap, ifrs-full, dei, srt<br/>
  --units UNITS         USD or shares<br/>
  --fact FACT           fact to collect e.g AccountsPayableCurrent, USD-per-<br/>
                        shares<br/>
  --directory DIRECTORY<br/>
                        directory to store the output<br/>
  --file FILE           file in which to store the output argument allowed for<br/>
                        each query type if --directory is not provided, it<br/>
                        should be the full path<br/>
  --companyconcept      returns all the XBRL disclosures from a single company<br/>
                        --cik required --frame - default us-gaap --fact -<br/>
                        default USD-per-shares<br/>
  --companyfacts        aggregates one fact for each reporting entity that is<br/>
                        last filed that most closely fits the calendrical<br/>
                        period requested --cik required<br/>
  --xbrlframes          returns all the company concepts data for a CIK --cy<br/>
                        required<br/>
  --companyfactsarchivezip<br/>
                        returns daily companyfacts index in a zip file<br/>
  --submissionszip      returns daily index of submissions in a zip file<br/>
  --financialstatementandnotesdataset<br/>
                        returns zip file with financial statement and notes<br/>
                        summaries --cy required<br/>
## edgarlatest10K<br/>
<br/>
usage: edgarlatest10K [-h] --cik CIK [--link] [--directory DIRECTORY]<br/>
<br/>
find the most recent 10-K for cik<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --cik CIK             10-digit Central Index Key<br/>
  --link                return the url for the latest 10-K<br/>
  --directory DIRECTORY<br/>
                        directory to store the output<br/>
## edgarlatestsubmissions<br/>
<br/>
usage: edgarlatestsubmissions [-h] --cik CIK [--directory DIRECTORY]<br/>
                            [--file FILE]<br/>
<br/>
find the most recent submissions for cik<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --cik CIK             10-digit Central Index Key<br/>
  --directory DIRECTORY<br/>
                        directory to store the output<br/>
  --file FILE           json file to process<br/>
<br/>
## edgarsubmissions<br/>
<br/>
usage: edgarsubmissions [-h] --cik CIK [--year YEAR] [--file FILE]<br/>
                      [--directory DIRECTORY]<br/>
<br/>
find the most recent submissions for cik<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --cik CIK             10-digit Central Index Key<br/>
  --year YEAR           year to search for submissions if not current year<br/>
  --file FILE           store the output in this file<br/>
  --directory DIRECTORY<br/>
                        store the output in this directory<br/>
<br/>
## edgarsubmissionsziptocsv<br/>
<br/>
usage: edgarsubmissionsziptocsv [-h] [--zipfile ZIPFILE] [--directory DIRECTORY]<br/>
                              [--files FILES]<br/>
<br/>
Extract one or more json files from an SEC EDGAR submissions.zip file and<br/>
convert to CSV<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --zipfile ZIPFILE     submissions.zip file to process - required<br/>
  --directory DIRECTORY<br/>
                        where to deposit the output<br/>
  --files FILES         comma separated(no spaces) content file(s) to process<br/>
                        a subset of the files in the zip file<br/>
<br/>
## edgarxbrlframestocsv<br/>
<br/>
usage: edgarxbrlframestocsv [-h] --file FILE [--directory DIRECTORY]<br/>
<br/>
Parse an SEC EDGAR xbrlframes json file after it has been altered to deal with<br/>
its multipart character and generate a csv file from its contents<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --file FILE           xbrl frames json file to process<br/>
  --directory DIRECTORY<br/>
                        where to deposit the output<br/>

