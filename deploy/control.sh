#!/bin/bash
case $1 in
    "build" )
        docker build -t rememberball_img ./
    ;;
    "run" )
        docker run --restart unless-stopped -d -v /home/rememberball/rememberball/data/:/root/rememberball/data/ --name rememberball rememberball_img
    ;;
    "stop" )
        docker stop rememberball
    ;;
    "rm" )
        docker rm rememberball
    ;;
    "rmi" )
        docker rmi rememberball_img
    ;;
    "rebuild" )
        docker stop rememberball
        docker rm rememberball
        docker rmi rememberball_img
        docker build -t rememberball_img ./
        docker run --restart unless-stopped --link redis-rejson:rejson --link some-mongo:mongo -d -v /home/rememberball/rememberball/data/:/root/rememberball/data/ --name rememberball rememberball_img
    ;;
    "inter")
        docker run -it --entrypoint /bin/bash --link redis-rejson:rejson --link some-mongo:mongo -v /home/rememberball/rememberball/data/:/root/rememberball_kek/data/ --name ememberball rememberball_img
    ;;
esac

