# Talk
-----------
Talk is a real time peer to peer video chat application. peer to peer means there is no server involment during data transmission. 
WebRTC is an amazing technology that make it possible. Even though data transmission is peer to peer but we will need a signalling mechanishm to initiate the communication (i.e. exchanging ip's,port numbers,video formats,codecs and other metadata related to video stream ). I've used websockets for signalling. 
There is a [live demo](https://sachinsngh165.github.io/talk/) of this project.

Usage:
- Enter a room id (it should be unique)
- Click join
- Share room id with friend and follow above two step
Enjoy!

> NOTE: This project just demonstrate the working of WebRTC. Security concerns are ignored & are in TODO list.

References:
- https://linuxconfig.org/how-to-setup-nginx-reverse-proxy
- https://onepagezen.com/letsencrypt-auto-renew-certbot-apache/
- https://www.nginx.com/blog/setting-up-nginx/
- https://medium.com/@ThomasTan/installing-nginx-in-mac-os-x-maverick-with-homebrew-d8867b7e8a5a
- https://www.freecodecamp.org/news/how-to-get-https-working-on-your-local-development-environment-in-5-minutes-7af615770eec/
- https://en.wikipedia.org/wiki/X.509
- https://stackoverflow.com/questions/4811738/how-to-log-cron-jobs

