#!/bin/bash

docker ps -aq | xargs docker rm -f
