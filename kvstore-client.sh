#!/bin/bash


usage ()
{
  echo "usage: $0 [-get] | [-put] | [-watch]"
  echo '''Example: 

To Put a value 
kvstore-client.sh -put foo bar 

To Get a value 
kvstore-client.sh -get foo 

To Get a value 
kvstore-client.sh -watch 
  '''  
exit 1
}

HOST=http://127.0.0.1:5000

METHOD=$1
KEYMESSAGE=$2
VALUEMESSAGE=$3

postmessage () {
  curl $HOST/put -d "key=$1&value=$2"
}

getmessage () {
  curl $HOST/get -d "key=$1"  
}

kvorgfile_update() {
  curl -s $HOST/watch > /tmp/.kvstore_orgdata
}  

kvorgnewfile_update() {
  curl -s $HOST/watch > /tmp/.kvstore_newdata
}

publishmsg() {
  cat /tmp/.kvstore_orgdata
}

watchmessage () {
  while true; do
     kvorgnewfile_update
     differ=$(diff /tmp/.kvstore_newdata /tmp/.kvstore_orgdata)
     kvorgfile_update

     if [ "$differ" != "" ] ; then
       kvorgfile_update
       publishmsg
     fi 

     sleep 1

  done

  return 0
}

case $METHOD in

   -get | -GET ) 
      if [ -z "$KEYMESSAGE" ]; then 
         usage
         exit 1
      else
         getmessage $KEYMESSAGE
      fi
   ;;

   -put | -PUT )
      if [ -z "$VALUEMESSAGE" ] ; then
          usage 
          exit 1
      else
          postmessage $KEYMESSAGE $VALUEMESSAGE
      fi
   ;;

   -watch | -WATCH )

      kvorgfile_update
      kvorgnewfile_update
      publishmsg
      watchmessage      

esac
