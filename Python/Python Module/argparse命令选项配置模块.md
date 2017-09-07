#argparse 
----


```
parse = argparse.ArgumentParser(description="Socket Server Example with select")
parse.add_argument('--name', action="store", dest="name", required = True)
parse.add_argument('--port', action='store', dest="port", type=int, required=True)
give_args = parse.parse_args()
port = give_args.port
name = give_args.name
```
