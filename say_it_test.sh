#!/bin/bash +xv
if [ -z "$HASHPIPE_BIN" ];
then
	echo HASHPIPE_BIN not defined!
	exit 1
fi

killall $HASHPIPE_BIN # seem to hang around last time

BOT_NAME="meetingbot"
BOT_SERVER="irc.mozilla.org"
BOT_CHANNEL='#rust-community'
BOT_CHANNEL='#sekrit31337'
BOT_MESSAGE=$@

echo ${BOT_MESSAGE} | $HASHPIPE_BIN --nick ${BOT_NAME} --server ${BOT_SERVER} --channels ${BOT_CHANNEL}
