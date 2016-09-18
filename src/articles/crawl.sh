#!/bin/bash
# crawl.sh

rm *.jl
 #scrapy crawl nba -o nba.jl
 #&
 #scrapy crawl fox -o fox.jl
scrapy crawl cbs -o cbs.jl &
scrapy crawl reuters -o reuters.jl &
scrapy crawl pbs -o pbs.jl &
scrapy crawl politico -o politico.jl &
wait
#pypy dataChecker.py
