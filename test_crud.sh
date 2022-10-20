#!/bin/bash

echo "Testing GET http://localhost:5000/"
curl http://localhost:5000/
echo

echo "Testing POST http://localhost:5000/ without auth"
curl -F file=@uploadme.txt http://localhost:5000/
echo

echo "Testing POST http://localhost:5000/ with auth"
curl -F file=@uploadme.txt http://localhost:5000/ -u "test:pass"
echo

echo "Testing POST http://localhost:5000/ with wrong auth"
curl -F file=@uploadme.txt http://localhost:5000/ -u "wrong:password"
echo

echo "Testing DELETE http://localhost:5000/ "
curl -X DELETE http://localhost:5000/
echo
