#!/bin/bash

echo "Testing GET http://localhost:5000/"
curl http://localhost:5000/
echo

echo "Testing POST http://localhost:5000/ without auth"
curl -X POST http://localhost:5000/ \
   -H "Content-Type: application/json"\
   -d '{"foo": "bar"}'
echo

echo "Testing POST http://localhost:5000/ with auth"
curl -X POST http://localhost:5000/ \
   -H "Content-Type: application/json"\
   -d '{"foo": "bar"}'\
   -u "test:pass"
echo

echo "Testing POST http://localhost:5000/ with wrong auth"
curl -X POST http://localhost:5000/ \
   -H "Content-Type: application/json"\
   -d '{"foo": "bar"}'\
   -u "wrong:password"
echo

echo "Testing DELETE http://localhost:5000/ "
curl -X DELETE http://localhost:5000/
echo
