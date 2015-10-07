for pid in `ps -ef|grep 'uwsgi'|awk '{print $2}'`
do
    echo $pid
    kill -9 $pid
done


nohup uwsgi -i wsgi.ini&
