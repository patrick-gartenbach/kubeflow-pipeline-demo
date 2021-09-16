for ((x=0; x<3; x++)); do
        if (($x == 0))
        then
                TAXIART="yellow"
        elif (($x == 1))
        then
                TAXIART="green"
        elif (($x ==  2))
        then
                TAXIART="fhv"
        fi
        echo $TAXIART

        for ((i=1; i<=12; i++)); do
                if(($i<10))
                then
                        MONAT="0$i"
                else
                        MONAT="$i"
                fi
                echo $MONAT
                wget "https://s3.amazonaws.com/nyc-tlc/trip+data/${TAXIART}_tripdata_2018-${MONAT}.csv"
        done
done