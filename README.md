# devops_pipeline
Think of a flask application as a restaurant : 

flask app= the kitchen 
endpoint= the serving window(each window serves something different)
request=your order
response=what you get back

Every time you type a URL in your browser , you re making a request to a specific endpoint, and the server sends back a response.

Each @app.route(...) in the code defines one of those windows:
/   -> "Hello, the server is running"
/health  ->"Yes, I'm up an healthy"
/time -> "Current time iss 14:32:05"
/tasks -> "Here are your tasks" (GET) or "Task added!"(Post) . The difference between get and post is that get is used when you re asking for something and post is used when you're senfing something