# dic_exec_3
```
docker build -t myapp .
docker run -d -p 5000:5000 myapp
```

# requests

```
 curl -X POST -d "@content.json" http://{aws_public_ip}:5000/api/detect
# multiple images
 curl -X POST -d "@content_multiple.json" http://{aws_public_ip}:5000/api/detect
```
