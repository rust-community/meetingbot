#!/bin/bash
endings=("bippity beep!" "boopity boop!" "*happy bleeping noises*" "blort!" "beep boop!")
rando=$(( ( RANDOM % 5 )  + 1 ))
URL="https://users.rust-lang.org/t/twir-friends-of-the-forest/7295"
MESSAGE="Time to check the TWIR Friends of the Forest thread! ${URL} ${endings[${rando}]}"
echo "DEBUG|Sending ${MESSAGE}"

/home/booyaa/meetingbot/doit.sh ${MESSAGE}
