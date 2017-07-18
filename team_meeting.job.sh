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

endings=("bippity beep!" "boopity boop!" "*happy bleeping noises*" "blort!" "beep boop!")
rando=$(( ( RANDOM % 5 )  + 1 ))
MESSAGE="$AGENDA The meeting is on Weds @ 4PM and 11PM UTC. ${endings[${rando}]}"
echo "DEBUG|Sending ${MESSAGE}"

/home/booyaa/meetingbot/say_it.sh ${MESSAGE}
