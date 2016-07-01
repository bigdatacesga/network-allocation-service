curl -H "Content-Type: application/json" -X POST -d @admin-network.json http://networks:5000/v1/networks

curl http://networks:5000/v1/networks/admin | python -mjson.tool
curl http://networks:5000/v1/networks/admin/addresses | python -mjson.tool
curl http://networks:5000/v1/networks/admin/addresses?full | python -mjson.tool
curl http://networks:5000/v1/networks/admin/addresses?free | python -mjson.tool
curl http://networks:5000/v1/networks/admin/addresses?free&full | python -mjson.tool
