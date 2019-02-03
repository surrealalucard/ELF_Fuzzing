for i in $(ps aux |grep radare2 |cut -d " " -f 4);do kill $i; done
