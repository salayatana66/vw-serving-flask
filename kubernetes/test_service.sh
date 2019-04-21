# Example of asking the server to predict with
# a curl command

while read -r line; do
curl --header "Content-Type: application/json" \
     --request POST \
     --data "$line"  \
     http://$1:6025/serve/;
echo "";
  done < json_test.json

