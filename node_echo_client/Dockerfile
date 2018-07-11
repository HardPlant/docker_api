FROM ubuntu

ARG echo_server_ip="192.168.0.100"
ENV echo_ip_server=$echo_server_ip

CMD ["curl", $echo_ip_server:5000, ""]