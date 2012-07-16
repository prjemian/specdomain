#!/bin/bash
# $Id$

# Use this script to (re)publish the documentation

export PROJECT="specdomain"
export MAKE_DIR="doc"
export SOURCE_DIR="_build"
export TARGET_DIR="/home/joule/SVN/subversion/bcdaext/"
export MAKE_TARGET="html"
#export PATH="/APSshare/epd/rh5-x86/bin:$PATH"

echo "Updating from subversion repository"
svn update

cd $MAKE_DIR
echo "rebuilding the documentation"
make clean
make $MAKE_TARGET

cd $SOURCE_DIR
echo "Removing the old build, if it exists"
/bin/rm -rf $PROJECT

echo "Copying the rebuilt web site"
mv html $PROJECT
tar cf /tmp/ball.tar $PROJECT
cd $TARGET_DIR
tar xf /tmp/ball.tar
echo "Done publishing $PROJECT"
