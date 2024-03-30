#! /bin/bash
set -ex

echo $EQDIR
echo $EQODIR
PD=src/edgarquery

# big files
# python ${PD}/doquery.py --companyfactsarchivezip \
#                                             --cik 1018724
# python ${PD}/doquery.py --submissionszip
python ${PD}/doquery.py --submissionszip
#sleep 5

python ${PD}/submissionsziptocsv.py --zipfile $EQODIR/submissions.zip \
    --files CIK0000831001.json,CIK0001665650.json,CIK0000019617.json

# SEC needs a user-agent
curl --user-agent $EQEMAIL --output /private/tmp/sitemap.xml \
     https://www.sec.gov/Archives/edgar/daily-index/sitemap.xml
curl --user-agent $EQEMAIL --output /private/tmp/company_tickers.json \
     https://www.sec.gov/files/company_tickers.json
for f in company.idx crawler.idx form.idx master.idx \
         xbrl.idx sitemap.quarterlyindexes.xml; do
    curl --user-agent $EQEMAIL --output $EQODIR/$f \
         https://www.sec.gov/Archives/edgar/full-index/$f
done


for cik in 1318605 1018724 1045810; do
    python ${PD}/doquery.py --companyfacts --cik $cik
done

for fct in AccountsPayableCurrent EarningsPerShareBasic; do
    python ${PD}/doquery.py --companyconcept --cik 1318605 --fact $fct
    python ${PD}/doquery.py --companyconcept --cik 1018724 --fact $fct
    python ${PD}/doquery.py --companyconcept --cik 1045810 --fact $fct
done

for fct in AccountsPayableCurrent AssetsCurrent DebtCurrent \
    LongTermDebt ; do
    for CY in CY2009Q2I CY2023Q1I CY2023Q2I CY2023Q3I; do
        echo $CY
        python ${PD}/doquery.py --xbrlframes --cy $CY --fact $fct
    done
done

for F in $(ls $EQODIR/CompanyFacts*.json |xargs basename); do
    echo $F
    python ${PD}/companyfactstocsv.py --file $EQODIR/$F --directory $EQODIR
done

for F in $(ls $EQODIR/CompanyConcept*.json |xargs basename); do
    echo $F
    python ${PD}/companyconcepttocsv.py --file $EQODIR/$F --directory $EQODIR
done

for F in $(ls $EQODIR/XBRLFrames*.json |xargs basename); do
    echo $F
    python ${PD}/xbrlframestocsv.py --file $EQODIR/$F --directory $EQODIR
done

#python ${PD}/submissionszipṫocsv.py --zipfile $EQODIR/submissions.zip --all


for cik in 5981 1318605 1018724 1045810; do
    #python ${PD}/latest10K.py --cik $cik
    #python ${PD}/latestsubmissions.py --cik $cik
    python ${PD}/submissions.py --cik $cik
    python ${PD}/submissions.py --cik $cik --year 2022
done

python ${PD}/tickerstocsv.py

##############################################################################
exit
##############################################################################



