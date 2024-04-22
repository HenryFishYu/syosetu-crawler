# syosetu crawler
### This is a project to fetch data from syosetu website, such as
https://ncode.syosetu.com \
https://noc.syosetu.com 

### How to run it
Example:
```
pip3 install -r requirements.txt
python3 crawler.py --url https://ncode.syosetu.com/n9066iw/ --interval 3
```
Help:
```
python3 crawler.py --help
```

| Parameter      | Comment                                 | Example                             | Required  | Default Value |
|----------------|-----------------------------------------|-------------------------------------|-----------|---------------|
| --url          | the url of target webpage               | https://ncode.syosetu.com/n9066iw/  | True      | N/A           |
| --interval     | the interval of each request in seconds | 2.0                                 | False     | 0             |
