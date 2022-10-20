#!/bin/bash

echo "Testing POST http://localhost:5000/ without auth"
curl -F file=@uploadme.txt http://localhost:5000/
echo

echo "Testing POST http://localhost:5000/ with wrong auth"
curl -F file=@uploadme.txt http://localhost:5000/ -u "wrong:password"
echo

echo "Testing POST http://localhost:5000/ with auth"
HASH=$(curl -F file=@uploadme.txt http://localhost:5000/ -u "test:pass")
echo

echo "Testing GET wrong hash from http://localhost:5000/"
wget -O $HASH.downloaded http://localhost:5000/wrong_hash
echo

echo "Testing GET $HASH from http://localhost:5000/"
wget -O $HASH.downloaded http://localhost:5000/$HASH
echo

echo "Testing DELETE http://localhost:5000/ "
curl -X DELETE http://localhost:5000/
echo
