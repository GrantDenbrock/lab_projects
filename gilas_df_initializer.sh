EXT=stats
for i in *.${EXT}; do
    cat $i | cut -f 2 >> $i.data.txt
done
