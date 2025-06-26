ES_HOST="http://new-es.endpoint:9200"
INPUT_DIR="./esdump"

for mapping_file in "$INPUT_DIR"/*_mapping.json; do
  index_name=$(basename "$mapping_file" | sed 's/_mapping.json//')
  data_file="$INPUT_DIR/${index_name}_data.json"

  echo "Restoring index: $index_name"

  elasticdump \
    --input="$mapping_file" \
    --output="$ES_HOST/$index_name" \
    --type=mapping

  elasticdump \
    --input="$data_file" \
    --output="$ES_HOST/$index_name" \
    --type=data
done
