export DB_NAME=cosmocargo
export DB_USER=cosmocargo_service
export DB_PASSWORD=cosmocargo
export DB_HOST=localhost
export DB_PORT=5432
python3 ../src/etl/etl.py ../data/sample_data.json >> ../logs/etl.log 2>&1 