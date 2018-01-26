#!/bin/bash
NEXT_MEETING=$(date --date="this wednesday" +"%Y-%m-%d")
LAST_WEEK=$(date --date="last wednesday" +"%Y-%m-%d")
echo "DEBUG|Last week: ${LAST_WEEK} This week: ${NEXT_MEETING}"

ISSUE=$($CATHULHU_CARGO_BIN issues rust-community/team --list | grep -iE '(meeting|agenda)' | grep $NEXT_MEETING | head -n 1)
# Does the minutes match last week date stamp
RESULT=$(echo $ISSUE | grep $NEXT_MEETING)
if [ $? -eq 0 ];
then
	echo "DEBUG|Found agenda!"
	AGENDA="This week's agenda: $(echo ${ISSUE} | cut -f3 -d'|')."
else
	echo "DEBUG|No agenda!"
	AGENDA="No agenda has been set! :("
fi

endings=("*hums the Final Countdown*" "bippity beep!" "boopity boop!" "*happy bleeping noises*" "blort!" "beep boop!")
roni=${#endings[@]}
rando=$(( ( RANDOM % ${roni} ) ))
MESSAGE="$1 ${endings[${rando}]}"
echo "DEBUG|Sending ${MESSAGE}"

/home/booyaa/meetingbot/say_it.sh ${MESSAGE}
