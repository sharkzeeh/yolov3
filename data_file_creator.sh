#!/bin/sh

cd data/

touch "wider.names"
echo "persons" > wider.names

touch "wider.data"
printf "%s\n" "classes=1" > wider.data
printf "%s\n" "train=data/train.txt" >> wider.data
printf "%s\n" "valid=data/valid.txt" >> wider.data
printf "%s" "names=data/wider.names" >> wider.data

cd ../