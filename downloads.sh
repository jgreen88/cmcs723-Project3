#!/bin/sh

#curl -Ss http://ttic.uchicago.edu/~wieting/paragram-phrase-XXL.zip > file.zip
#unzip file.zip
#rm file.zip

curl https://doc-14-7c-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/3l68emgbv4jvpr4o6ghm5kllbpigtrog/1481601600000/14570458592396221227/*/0B9w48e1rj-MOck1fRGxaZW1LU2M?e=download > file.zip
unzip file.zip
rm file.zip
mv paragram_300_sl999/* .
rm README.txt
rm file.gz
rm -rf paragram_300_sl999

