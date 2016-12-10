#!/bin/sh

curl -Ss http://ttic.uchicago.edu/~wieting/paragram-phrase-XXL.zip > file.zip && \
unzip file.zip && \
rm file.zip

curl -Ss https://doc-08-3k-docs.googleusercontent.com/docs/securesc/bj1odvti56n9sbh18h25t4deksvrrk7u/v2n9ecorfe3phc7n9e02nt38rlf3dm53/1481385600000/06848720943842814915/03078941804631754256/0B7XkCwpI5KDYNlNUTTlSS21pQmM?e=download&h=04969168175474109593&nonce=mc652j3i9p2oo&user=03078941804631754256&hash=ev63pk1juf595lvsbie49659g10kli3p > file.gz && \
gunzip file.gz && \
rm file.gz
