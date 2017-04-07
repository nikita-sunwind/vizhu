#!/bin/bash

set -e

# Server hooks
cd ./server && invoke check test && cd ..

# Client hooks
cd ./client && npm run check && npm run webpack && npm run test && cd ..
