#|/bin/bash
[ $(( 10#`date +%W` %2 )) -eq 0 ] && true 
