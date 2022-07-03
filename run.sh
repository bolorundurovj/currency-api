python3 -m alembic upgrade head

PASS=$?
if [ $PASS == 0 ]; then
        python3 -m uvicorn web:app
else
    echo "alembic upgrade failed"
fi
