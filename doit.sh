#!/bin/bash +xv
CATHULHU_GIT_REPO=/path/to/repo/team
CATHULHU_CARGO_BIN=/path/to/cargo/bin

echo "DEBUG|cron's path: $PATH"

git -C $CATHULHU_GIT_REPO fetch
git -C $CATHULHU_GIT_REPO merge
echo "DEBUG|Updated repo"

DAY_NO=$(date +"%u")

#TEST
#DAY_NO=3 #testing
#echo "TEST|Overriding DAY_NO to 3 was " $(date +"%u")
if [ ! ${DAY_NO} -eq 3 ] && [ ! ${DAY_NO} -eq 2 ];
then
	echo Not Tuesday or Wednesday
	exit 1
fi

NEXT_MEETING=$(date --date="this wednesday" +"%Y-%m-%d")
LAST_WEEK=$(date --date="last wednesday" +"%Y-%m-%d")
echo "Last week: ${LAST_WEEK} Next week: ${NEXT_MEETING}"

#TEST
#echo "TEST|overriding $LAST_WEEK"
#LAST_WEEK='2016-09-21'

# what each line does in FILE_NAME
# 1 - get commits since last week
# 2 - find the "diff" lines (since they contain the file names)
#
# sample:
#
# diff --git a/meeting-minutes/2016-09-21.txt b/meeting-minutes/2016-09-21.txt
#
# 3 - find anything that looks like minutes
# 4 - grab the first line
# 5 - grab the file name
#
# sample:
#
# a/meeting-minutes/2016-09-21.txt
#
# 6 - strip the 'a'
FILE_NAME=$(git -C $CATHULHU_GIT_REPO log --oneline --decorate --after="${LAST_WEEK}" -p | \
	grep -E '^diff' | \
	grep -iE '(minute|meeting)' | \
	head -n 1 | \
	cut -d' ' -f3 | \
	sed 's/a//')

# Does the minutes match last week date stamp?
RESULT=$(echo $FILE_NAME | grep $LAST_WEEK)
if [ $? -eq 0 ];
then
	MINUTES="Last week's minutes https://github.com/rust-community/team/blob/master$FILE_NAME."
else
	MINUTES="No minutes found for last week. :("
fi
echo "Last weeks minutes: $RESULT"

#TEST
#echo "TEST|overriding $NEXT_MEETING"
#NEXT_MEETING='2016-09-28'

ISSUE=$($CATHULHU_CARGO_BIN/cathulhu issues rust-community/team --list | grep -iE '(meeting|agenda)' | head -n 1)
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

echo "DEBUG|result: $RESULT"
echo "DEBUG|issue: $ISSUE"
echo "DEBUG|last week: $LAST_WEEK"
echo "DEBUG|filename: $FILE_NAME"
echo "DEBUG|agenda: $AGENDA"

NICK=meetingbot
SERVER=irc.mozilla.org
CHANNEL=\#rust-community
#testing CHANNEL=\#sekrit382
MESSAGE="$AGENDA The meeting is this Weds @ 4PM UTC. $MINUTES bippity beep!"
echo "DEBUG|Sending ${MESSAGE}"

$CATHULHU_CARGO_BIN/mouthpiece -n $NICK -s $SERVER -c $CHANNEL -m "$MESSAGE"
