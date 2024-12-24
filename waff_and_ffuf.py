#!/bin/bash

input_file="httpx_results.txt"
wordlist="/path/to/wordlist.txt"

while read -r domain; do
    echo "Testing WAF for $domain..."
    waf=$(wafw00f -a https://$domain | grep "WAF:")

    if [[ $waf == *Cloudflare* ]]; then
        echo "Cloudflare detected. Adjusting ffuf parameters..."
        ffuf -u https://$domain/FUZZ \
        -w $wordlist \
        -t 1 \
        -rate 0.5 \
        --header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" \
        --header "CF-Access-Client-Id: your-cloudflare-client-id" \
        --header "CF-Access-Client-Secret: your-cloudflare-client-secret" \
        -o ${domain}_ffuf_results.txt
    else
        echo "Generic or no WAF detected. Running standard ffuf..."
        ffuf -u https://$domain/FUZZ \
        -w $wordlist \
        -t 1 \
        -rate 0.2 \
        --timeout 30 \
        -o ${domain}_ffuf_results.txt
    fi
done < $input_file
