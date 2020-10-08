## Sample Execution

Crawl coordinates contained on `amazonas-data` file only, extending zoom level (`-z`) to 9 and adding 400 concurrent conecctions.  To avoid ban check https://wiki.earthdata.nasa.gov/display/GIBS/GIBS+API+for+Developers#GIBSAPIforDevelopers-BulkDownloading

```
./geo-crawler.py dates.txt -z 9 -b amazonas-data -c 400
```