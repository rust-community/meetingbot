#!/bin/bash
endings=("*hums the Final Countdown*" "bippity beep!" "boopity boop!" "*happy bleeping noises*" "blort!" "beep boop!")
roni=${#endings[@]}
rando=$(( ( RANDOM % ${roni} ) ))
MESSAGE="$1 ${endings[${rando}]}"
echo "DEBUG|Sending ${MESSAGE}"

# if you want to test the output, define an env var called MEETINGBOT (value doesn't matter)
# this will skip sending to the irc
if [[ -z "$MEETINGBAWT" ]]; then 
  /home/booyaa/meetingbot/say_it.sh ${MESSAGE}
fi
