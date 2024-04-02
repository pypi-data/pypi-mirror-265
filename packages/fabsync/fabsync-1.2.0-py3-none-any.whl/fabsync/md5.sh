#!/bin/sh

# Prints the md5 digest of a given path, using whatever tool we can find.

if command -v md5sum >/dev/null; then  # GNU coreutils
    command md5sum -b "$1" | cut -d ' ' -f 1
elif command -v md5 >/dev/null; then   # BSD
    command md5 -q "$1"
elif command -v openssl >/dev/null; then
    command openssl md5 -r "$1" | cut -d ' ' -f 1
else
    exit 2
fi
