    function refreshReport()
    {
        q = $( '#q' ).val();
        $( '#results' ).html( '&nbsp;' ).load( '{% url "report_search" %}?q=' + q +"&rev=" + rev);
    }

    function refresh()
    {
        q = $( '#q' ).val();
        $( '#results' ).html( '&nbsp;' ).load( '{% url "search" %}?q=' + q +"&rev=" + rev);
    }

    function changeRev()
    {
        if (rev === 1)
            rev = 0;
        else
            rev = 1;
            refreshReport();
    }