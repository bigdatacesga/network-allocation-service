curl -H "Content-Type: application/json" -X POST -d @testnetwork.json http://127.0.0.1:5006/resources/networks/v1/networks/

curl 'http://127.0.0.1:5006/resources/networks/v1/networks/testnetwork' | python -mjson.tool

curl 'http://127.0.0.1:5006/resources/networks/v1/networks/testnetwork/addresses' | python -mjson.tool

curl 'http://127.0.0.1:5006/resources/networks/v1/networks/testnetwork/addresses?full' | python -mjson.tool

curl 'http://127.0.0.1:5006/resources/networks/v1/networks/testnetwork/addresses?free' | python -mjson.tool

curl 'http://127.0.0.1:5006/resources/networks/v1/networks/testnetwork/addresses?free&full' | python -mjson.tool
