#!/bin/bash

BUILD_DIR=build
RELEASE_DIR=release

function create_dir {
    FOLDER_NAME=$1
    if [ ! -d ${FOLDER_NAME} ]; then
        mkdir ${FOLDER_NAME}
    fi
}

# Find current branch
CURRENT=`git branch | grep '\*' | awk ' {print $2}'`

# Export current branch to build directory
create_dir ${BUILD_DIR}
git archive ${CURRENT} | tar -x -C ./build

# Copy required files to release directory
create_dir ${RELEASE_DIR}
cp -rfv ${BUILD_DIR}/modules/* ${RELEASE_DIR}/
cp -rfv ${BUILD_DIR}/pytaora ${RELEASE_DIR}/
cp -rfv ${BUILD_DIR}/taora ${RELEASE_DIR}/
cp -rfv ${BUILD_DIR}/.taora ${RELEASE_DIR}/
cp -rfv ${BUILD_DIR}/LICENSE ${RELEASE_DIR}/
cp -rfv ${BUILD_DIR}/README.md ${RELEASE_DIR}/
