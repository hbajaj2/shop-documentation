#!/bin/bash
echo -e "Content-type: text/html\n\n"


# (internal) routine to store POST data
function cgi_get_POST_vars()
{
    # check content type
    [ "${CONTENT_TYPE}" != "application/x-www-form-urlencoded" ] && \
    echo "bash.cgi warning: you should probably use MIME type "\
         "application/x-www-form-urlencoded!" 1>&2
    # save POST variables (only first time this is called)
    [ -z "$QUERY_STRING_POST" \
      -a "$REQUEST_METHOD" = "POST" -a ! -z "$CONTENT_LENGTH" ] && \
        read -n $CONTENT_LENGTH QUERY_STRING_POST
    # prevent shell execution
    local t
    t=${QUERY_STRING_POST//%60//} # %60 = `
    t=${t//\`//}
    t=${t//\$(//}
    t=${t//%24%28//} # %24 = $, %28 = (
    QUERY_STRING_POST=${t}
    return
}

# (internal) routine to decode urlencoded strings
function cgi_decodevar()
{
    [ $# -ne 1 ] && return
    local v t h
    # replace all + with whitespace and append %%
    t="${1//+/ }%%"
    while [ ${#t} -gt 0 -a "${t}" != "%" ]; do
    v="${v}${t%%\%*}" # digest up to the first %
    t="${t#*%}"       # remove digested part
    # decode if there is anything to decode and if not at end of string
    if [ ${#t} -gt 0 -a "${t}" != "%" ]; then
        h=${t:0:2} # save first two chars
        t="${t:2}" # remove these
        v="${v}"`echo -e \\\\x${h}` # convert hex to special char
    fi
    done
    # return decoded string
    echo "${v}"
    return
}

# routine to get variables from http requests
# usage: cgi_getvars method varname1 [.. varnameN]
# method is either GET or POST or BOTH
# the magic varible name ALL gets everything
function cgi_getvars()
{
    [ $# -lt 2 ] && return
    local q p k v s
    # prevent shell execution
    t=${QUERY_STRING//%60//} # %60 = `
    t=${t//\`//}
    t=${t//\$(//}
    t=${t//%24%28//} # %24 = $, %28 = (
    QUERY_STRING=${t}
    # get query
    case $1 in
    GET)
        [ ! -z "${QUERY_STRING}" ] && q="${QUERY_STRING}&"
        ;;
    POST)
        cgi_get_POST_vars
        [ ! -z "${QUERY_STRING_POST}" ] && q="${QUERY_STRING_POST}&"
        ;;
    BOTH)
        [ ! -z "${QUERY_STRING}" ] && q="${QUERY_STRING}&"
        cgi_get_POST_vars
        [ ! -z "${QUERY_STRING_POST}" ] && q="${q}${QUERY_STRING_POST}&"
        ;;
    esac
    shift
    s=" $* "
    # parse the query data
    while [ ! -z "$q" ]; do
    p="${q%%&*}"  # get first part of query string
    k="${p%%=*}"  # get the key (variable name) from it
    v="${p#*=}"   # get the value from it
    q="${q#$p&*}" # strip first part from query string
    # decode and evaluate var if requested
    [ "$1" = "ALL" -o "${s/ $k /}" != "$s" ] && \
        eval "$k=\"`cgi_decodevar \"$v\"`\""
    done
    return
}



# register all GET and POST variables
cgi_getvars BOTH ALL

#Place message post submit
echo "<pre>Your Request is getting processed, you will receive email shortly</pre>"
#setting custom variables for document generation task
cgi_dir=/var/www/cgi-bin
mkdir $cgi_dir/working
myyear=`date +'%Y'`
NOW=$(date +"%m-%d-%Y")
#Add task environment dropdown specific variables, so that they can be processed in loop
vars="prodwcs prodwcsauth prodwcsdb prodwcsauthdb prodwcsnodb prodwcsauthnodb burstwcs burstwcsauth burstwcsdb burstwcsauthdb burstwcsnodb burstwcsauthnodb proddataload prodauthdataload burstdataload burstauthdataload prodmsjobs prodauthmsjobs burstmsjobs burstauthmsjobs prodcq  prodwcspatch burstwcspatch burstupdatewrkspcauth produpdatewrkspcauth prodwxs burstwxs prodihs burstihs prodauthihs burstauthihs prodinternaltoolihs burstinternaltoolihs prodauthinternaltoolihs burstinternaltoolihs prodctrlm burstctrlm prodendeca burstendeca prodwcspatch prodwcsauthpatch burstwcspatch burstwcsauthpatch prodakamai100 prodakamai10 burstakamai100 burstakamai10 ctrlmprodonly ctrlmburstonly prodctrlmbau ihsbau prodwcsauthapar prodwcsapar burstwcsauthapar burstwcsapar prodshutdownjvms prodprofilebackup prodwcsbackup prodrestartjvms  burstshutdownjvms burstprofilebackup burstwcsbackup burstrestartjvms prodpropagateindexh8 burstpropagateindexh8 prodpropagateindexh5 burstpropagateindexh5   prodexecutebaseline burstexecutebaseline burstswitchworkbench8 prodswitchworkbench5 prodihstoreplica burstihstoreplica prodrestarth5wxs burstrestarth8wxs burstctrlmswitch  prodctrlmswitch prodcqconscheck  prodflashbackauth prodflashbacklive burstflashbackauth burstflashbacklive burstinternaltoolauth  prodinternaltoolauth burstinternaltoollive prodinternaltoollive  burstctrlmnightly  prodctrlmnightly proddatagaurdauth proddatagaurdlive proddatagaurdenable prodcreaterestorepointlive prodcreaterestorepointauth  sit3wcs sit3wcsauth sit3wcsdb sit3wcsauthdb sit3wcsnodb sit3wcsauthnodb sit3bwcs sit3bwcsauth sit3bwcsdb sit3bwcsauthdb sit3bwcsnodb sit3bwcsauthnodb sit3dataload sit3authdataload sit3bdataload sit3bauthdataload sit3msjobs sit3authmsjobs sit3bmsjobs sit3bauthmsjobs sit3cq  sit3wcspatch sit3bwcspatch sit3bupdatewrkspcauth sit3updatewrkspcauth sit3wxs sit3bwxs sit3ihs sit3bihs sit3authihs sit3bauthihs sit3internaltoolihs sit3binternaltoolihs sit3authinternaltoolihs sit3binternaltoolihs sit3ctrlm sit3bctrlm sit3endeca sit3bendeca sit3wcspatch sit3wcsauthpatch sit3bwcspatch sit3bwcsauthpatch sit3akamai100 sit3akamai10 sit3bakamai100 sit3bakamai10 ctrlmsit3only ctrlmsit3bonly sit3ctrlmbau sit3ihsbau sit3wcsauthapar sit3wcsapar sit3bwcsauthapar sit3bwcsapar sit3shutdownjvms sit3profilebackup sit3wcsbackup sit3restartjvms  sit3bshutdownjvms sit3bprofilebackup sit3bwcsbackup sit3brestartjvms sit3propagateindexh8 sit3bpropagateindexh8 sit3propagateindexh5 sit3bpropagateindexh5   sit3executebaseline sit3bexecutebaseline sit3bswitchworkbench8 sit3switchworkbench5 sit3ihstoreplica sit3bihstoreplica sit3restarth5wxs sit3brestarth8wxs sit3bctrlmswitch  sit3ctrlmswitch DRwcs DRwcsauth DRwcsdb DRwcsauthdb DRwcsnodb DRwcsauthnodb DRdataload DRauthdataload DRmsjobs DRauthmsjobs DRcq  DRwcspatch DRupdatewrkspcauth DRwxs DRihs DRauthihs DRinternaltoolihs DRauthinternaltoolihs DRctrlm DRendeca DRwcspatch DRwcsauthpatch DRakamai100 DRakamai10 ctrlmDRonly DRctrlmbau DRwcsauthapar DRwcsapar DRshutdownjvms DRprofilebackup DRwcsbackup DRrestartjvms DRpropagateindextolive  DRexecutebaseline DRswitchworkbench5 DRihstoreplica DRrestarth5wxs DRctrlmswitch sit3flashbackauth sit3flashbacklive sit3createrestorepointlive sit3createrestorepointauth sit3logicaldbrollbacklive sit3logicaldbrollbackauth sit3ctrlmnightly sit3internaltoollive sit3internaltoolauth sit3bwcsdb1 sit3bwcsauthdb1 sit3cqconscheck sit3ctrlmnightly2 DRsharedmountsnapmirror DRdatagaurdchange DRrestartcms DRenabledatagaurdwxs sit3bupdatefixpackdb sit3bwcs70backup sit3bwcsfixpackinstallinstancelevel sit3bwcsfixpackinstallproductlevel sit3bwcsupdiinstal  sit3bpermissionwcs sit3bbatchsync sit3updatefixpackdb sit3wcs70backup sit3wcsfixpackinstallinstancelevel sit3wcsfixpackinstallproductlevel sit3wcsupdiinstal  sit3permissionwcs sit3batchsync prodwcs70backup prodwcsupdiinstal prodwcsfixpackinstallproductlevel prodwcsfixpackinstallinstancelevel produpdatefixpackdb prodpermissionwcs prodbatchsync DRwcs70backup DRwcsupdiinstal DRwcsfixpackinstallproductlevel DRwcsfixpackinstallinstancelevel DRupdatefixpackdb DRpermissionwcs DRbatchsync burstwcs70backup burstwcsupdiinstal burstwcsfixpackinstallproductlevel  burstwcsfixpackinstallinstancelevel burstupdatefixpackdb burstpermissionwcs burstbatchsync"
for var in $vars
do
 if [ -z ${!var} ] 
       then 
        echo  
      else
#	echo "The value of variable ${var} is ${!var}" 
	var1=$(awk -F_ '{ print $1}' <<<"${!var}")
#	var2=$(awk -F_ '{gsub(/[ \t]+$/, "", $2); print $2 ""}' <<<"${!var}")
	var2=$(awk -F_ '{ print $2}' <<<"${!var}")
	var3=$(awk -F_ '{gsub(/[ \t]+$/, "", $3); print $3 ""}' <<<"${!var}")
	EV="${var}_ev"
	RL="${var2}_RL"
        RTAG="$Branch"_"${!RL}" 	
	var4="${var2}${var3}"
	#echo "${var4}"
	cp $cgi_dir/template/${var4}.txt $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	sed -i "s/&wcs_ev&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	sed -i "s/&endeca_ev&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	sed -i "s/&ihs_ev&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	sed -i "s/&dataload_ev&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	sed -i "s/&ctrlm_ev&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	sed -i "s/&msjobs_ev&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
        sed -i "s/&cq_ev&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
        sed -i "s/&wxs_ev&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	sed -i "s/&EV&/${!EV}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
 	sed -i "s/&BRANCH&/$RTAG/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	sed -i "s/&RL&/${!RL}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	if [ $var == "DRwcs" ] || [ $var == "DRwcsauth" ]; then
		if [ $var == "DRwcs" ]; then
			var9="drcheck"
		fi
	        if [ $var == "DRwcsauth" ]; then
                	var9="drcheckauth"
        	fi
		sed -i "s/&ENV&/$var9/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	else
		sed -i "s/&ENV&/$var1/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
	fi
        if [ "$var" == "prodihs" ] || [ "$var" == "burstihs" ] || [ "$var" == "sit3ihs" ] || [ "$var" == "sit3bihs" ] || [ "$var" == "prodihstoreplica" ] || [ "$var" == "burstihstoreplica" ] || [ "$var" == "sit3ihstoreplica" ] || [ "$var" == "sit3bihstoreplica" ]; then
                if [ "$var" == "prodihs" ] || [ "$var" == "prodihstoreplica" ]; then
                        HALL="hall5"
                fi
                if [ "$var" == "burstihs" ] || [ "$var" == "burstihstoreplica" ]; then
                        HALL="hall8"
                fi
                if [ "$var" == "sit3ihs" ] || [ "$var" == "sit3ihstoreplica" ]; then
                        HALL="sit3"
                fi
                if [ "$var" == "sit3bihs" ] || [ "$var" == "sit3bihstoreplica" ]; then
                        HALL="sit3b"
                fi
                sed -i "s/&hall&/${HALL}/g" $cgi_dir/working/${!EV}_${var1}_${var4}.txt
        fi
      fi	
done
#Capturing comment as input for the options not available within dropdown
comments="comment1 comment2 comment3 comment4 comment5 comment6 comment7 comment8 comment9 comment10 comment11 comment12 comment13 comment14 comment15 comment16 sit3comment1 sit3comment2 sit3comment3 sit3comment4 sit3comment5 sit3comment6 sit3comment7 sit3comment8 DRcomment1 DRcomment2 DRcomment3 DRcomment4 DRcomment5 DRcomment6 DRcomment7 DRcomment8  sit3comment9 sit3comment10 sit3comment11 sit3comment12 sit3comment13 sit3comment14 sit3comment15 sit3comment16 sit3comment17 sit3comment18 sit3comment19 sit3comment20 sit3comment21 sit3comment22 sit3comment23 sit3comment24 DRcomment9 DRcomment10 DRcomment11 DRcomment12 DRcomment13 DRcomment14 DRcomment15 DRcomment16 comment17 comment18 comment19 comment20 comment21 comment22 comment23 comment24"
for comment in $comments
do
  if [ -z "${!comment}" ]
	then
	 echo  
	else	
	#echo "The value of variable ${comment} is ${!comment}"
	ComEV="${comment}_ev"
	echo "${!comment}" > $cgi_dir/working/${!ComEV}_comment.txt
	sed -i "1s/^/${!ComEV} /g" $cgi_dir/working/${!ComEV}_comment.txt
	sed -i "s/\\r/\\n/g" $cgi_dir/working/${!ComEV}_comment.txt
       fi	
done

#Merge and email task
	cp $cgi_dir/template/${ENV}.txt $cgi_dir/working/98_${ENV}.txt
	cp $cgi_dir/template/${ENV}_1.txt $cgi_dir/working/99_${ENV}.txt
	cp  $cgi_dir/template/0_header.txt $cgi_dir/working/
	sed -i "s/&ENVN&/$ENV/g" $cgi_dir/working/0_header.txt
	sed -i "s/&NOW&/${NOW}/g" $cgi_dir/working/0_header.txt
	cd $cgi_dir/working
	echo "Table of Content" > 0_toc.txt
	grep -h "^[1-9]" [1-9]*.txt | sort -V  >> 0_toc.txt
	grep -h "^Appendix" 9[8-9]*.txt >> 0_toc.txt
	for i in `ls *.txt | sort -V`
	do 
	pr -F $i >> impplan.txt
	done
	sed -i "/^$myyear/d" impplan.txt
	sed -i "s/Trunk_//g" impplan.txt
	enscript -B impplan.txt --output=- | ps2pdf - > imp_plan.pdf
#	enscript -B -f "Times-Roman10" -F "Times-Bold18" impplan.txt --output=- | ps2pdf - > imp_plan.pdf
#	mailx -r docgeneration@sapient.com -a imp_plan.pdf -s "Implementation Plan for $ENV" -c hbajaj2@Sapient.com $email_id < $cgi_dir/mailnote
	mailx -r docgeneration@sapient.com -a imp_plan.pdf -s "Implementation Plan for $ENV" -b hbajaj2@sapient.com $email_id < $cgi_dir/mailnote
	rm -rf $cgi_dir/working/
cat <<EOF
</body>
</html>
EOF
