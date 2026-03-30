FROM nginx:latest

LABEL maintainer="nsh"
LABEL description="Custom NGINX web server for E1-1 assignment"

# 환경 변수
ENV AUTHOR="nsh" \
    COURSE="DevOps E1-1"

# 커스텀 index.html 복사
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
