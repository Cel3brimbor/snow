#!/bin/bash

cleanup() {
    echo "Cleaning up..."
    rm -rf /tmp/java-build
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

lsof -ti:8000 | xargs kill -9 2>/dev/null || true
sleep 1

#create temp dir
mkdir -p /tmp/java-build

javac -d /tmp/java-build *.java objects/*.java webserver/*.java 2>&1

if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi

cd ..
java -cp /tmp/java-build backend.Main