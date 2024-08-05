from flask import Flask, jsonify,request
import psutil,time  
from prometheus_client import Histogram,Counter, generate_latest  
from prometheus_client import CollectorRegistry  
app = Flask(__name__)  

# CreateRegistry 
registry = CollectorRegistry()  

# Create a histogram to record the response times of requests.  
REQUEST_LATENCY = Histogram(  
    'http_request_duration_seconds',   
    'HTTP Request Latency',  
    ['method', 'endpoint'],  
    registry=registry    
)  
####record response status
http_status_counter = Counter(  
    'http_response_status_total',  
    'Total number of HTTP responses by status code',  
    ['method', 'endpoint', 'status_code'],  
    registry=registry  

)  



@app.before_request  
def before_request():  
    # Record the start time at the beginning of the request  
    # Initialize the status code before each request  
    request.start_time = time.time()  

@app.after_request  
def after_request(response):  
    # Record the status code
    http_status_counter.labels(method=request.method, endpoint=request.path, status_code=response.status_code).inc()  
    # Calculate the duration of the request
    latency = time.time() - request.start_time  
    # Record the response time in the histogram  
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(latency) 
    # Return the response
    return response  



@app.route('/metrics')  
def metrics():  
    # Expose the metrics 
    return generate_latest(registry)  



@app.route('/system_info', methods=['GET'])  
def system_info():  
    # Get CPU usage  
    cpu_usage = psutil.cpu_percent(interval=1)  
    
    # Get disk information  
    memory_info = psutil.virtual_memory()  
    
    # Construct return data 
    disk_info = psutil.disk_usage('/')  
    
    # Start Flask application  
    info = {  
        'cpu_usage_percent': cpu_usage,  
        'memory': {  
            'total': memory_info.total,  
            'available': memory_info.available,  
            'used': memory_info.used,  
            'percentage': memory_info.percent  
        },  
        'disk': {  
            'total': disk_info.total,  
            'used': disk_info.used,  
            'free': disk_info.free,  
            'percentage': disk_info.percent  
        }  
    }  

    print(info)
    
    return jsonify(info)  


if __name__ == '__main__':  
    # enable Flask flask
    app.run(host='0.0.0.0',port=8001, debug=True)