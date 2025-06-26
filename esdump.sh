ES_HOST="http://es.endpoint:9200"
OUTPUT_DIR="./esdump"

mkdir -p "$OUTPUT_DIR"

indices=$(curl -s "$ES_HOST/_cat/indices?h=index" | sort | uniq)

for index in $indices; do
  echo "Dumping index: $index"

  elasticdump \
    --input="$ES_HOST/$index" \
    --output="$OUTPUT_DIR/${index}_mapping.json" \
    --type=mapping

  elasticdump \
    --input="$ES_HOST/$index" \
    --output="$OUTPUT_DIR/${index}_data.json" \
    --type=data
done
