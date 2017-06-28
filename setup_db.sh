# this should be used for local development only
echo "CREATE USER poet WITH SUPERUSER PASSWORD 'poet123';" | psql
echo "CREATE DATABASE poet;" | psql
echo "CREATE DATABASE poet_test;" | psql
