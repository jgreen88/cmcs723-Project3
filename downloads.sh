#!/bin/sh

curl -Ss http://ttic.uchicago.edu/~wieting/paragram-phrase-XXL.zip > file.zip && \
unzip file.zip && \
rm file.zip
