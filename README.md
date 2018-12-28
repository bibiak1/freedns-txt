# freedns-txt
Python script made for easy txt record update on freedns.42.pl to allow letsencrypt.org wildcards challenge support.

If you want it to use with certbot it can be easly done with manual_auth_hook functionality.
e.g.

authenticator = manual
manual_auth_hook = /etc/letsencrypt/test

/etc/letsencrypt/test file:
DNS1=fns1.42.pl
DNS2=fns2.42.pl
COUNT=100
SLEEP=60
OUTFILE=/etc/letsencrypt/test.out

echo "${CERTBOT_DOMAIN} _acme-challenge TXT ${CERTBOT_VALIDATION}" > ${OUTFILE}
/usr/bin/python2 /etc/letsencrypt/freedns-txt.py -a -v "${CERTBOT_VALIDATION}" >> ${OUTFILE}
echo "start checking... (up to ${COUNT} * ${SLEEP}sec)" >> ${OUTFILE}
C=0; while [ ${C} -lt ${COUNT} -a -z "`host -t txt _acme-challenge.${CERTBOT_DOMAIN} ${DNS1} | grep ${CERTBOT_VALIDATION}`" -a -z "`host -t txt _acme-challenge.${CERTBOT_DOMAIN} ${DNS2} | grep ${CERTBOT_VALIDATION}`" ]; do echo -n ${C}... >> ${OUTFILE}; sleep ${SLEEP}; C=$(( C+1 )); done
echo >> ${OUTFILE}
(host -t txt _acme-challenge.${CERTBOT_DOMAIN} ${DNS1}; host -t txt _acme-challenge.${CERTBOT_DOMAIN} ${DNS2}) >> ${OUTFILE}
echo "sleeping 2 more minutes..." >> ${OUTFILE}
sleep 120
echo "script end" >> ${OUTFILE}
