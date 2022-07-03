python3 -m alembic upgrade head

PASS=$?
if [ $PASS == 0 ]; then
        python3 -u web.py
else
    echo "alembic upgrade failed"
fi
