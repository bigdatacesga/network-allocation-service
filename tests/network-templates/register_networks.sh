for NAME in admin storage networks disks paas framework mesos; do
    curl -H "Content-Type: application/json" -X POST -d @${NAME}-network.json http://networks:5000/v1/networks
done
