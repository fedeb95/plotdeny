# plotdeny
Run with `python3 plotdeny.py <path_to_file_with_ip_list>

I generated the file with
`for i in /var/log/denyhosts*;do cat $i |grep 'new denied'>>/root/denied.txt;done`

Dependencies:
pandas, requests, plotly
