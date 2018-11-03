# Pod 详解
---
yaml 格式的Pod 定义文件完整内容如下:
```
apiVersion: v1
kind: Pod
metadata:
  name: string
  namespace: string
  labels:
    - name: string
   aunnotations:
     - name: string
spec:
  containers:
    - name: string
      image: string
      imagePullPolicy: [Always | Never | IfNotPresent]
      command: [string]
      args: [string]
      workingDir: string
      volumeMounts: 
      - name: string
        mountPath: string
        readOnly: boolean
      ports:
      - name: string
        containerPort: int
        hostPort: int
        protocol: string
      env:
      - name: string
        value: string
      resources:
        limits:
          cpu: string
          memory: string
        requests:
          cpu: string
          memory: string
      livenessProbe:
        exec:
          command: [string]
        httpGet:
          path: string
          port: number
          host: string
          scheme: string
          httpHeaders:
          - name: string
            value: string
        tcpSocket:
          port: number
        initialDelaySeconds: 0
        timeoputSeconds: 0
        successThreshold: 0
        failureThreshold: 0
      securityContext:
        privileged: false
    restartPolicy: [Always | Never | OnFailture] 
    nodeSelector: object
    imagePullSecrets:
    - name: string
    hostNetwork: false
    volumes:
    - name: string
      emptyDir: {}
      hostPath:
        path: string
      secret:
        secretName: string
        items:
        - key: string
          path: string
       configMap:
       - name: string
         items:
         - key: string
           path: string 

```
