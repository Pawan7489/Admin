# File: backend/queue/upstash_kafka_queue.py
# Purpose: Manages the "Line" of 100+ users.
# Logic: Producer adds to line, Consumer processes one by one.

from confluent_kafka import Producer, Consumer
import json

class UpstashKafkaManager:
    def __init__(self, conf):
        """
        conf: Upstash Kafka Console se mili hui settings.
        (Bootstrap Server, SASL User/Pass).
        """
        self.conf = conf
        self.topic = "a1_job_queue"

    def add_to_queue(self, user_id, task_data):
        """
        PRODUCER: User ki request ko line mein lagata hai.
        """
        producer = Producer(self.conf)
        
        task_json = json.dumps({"user": user_id, "task": task_data})
        
        try:
            producer.produce(self.topic, key=user_id, value=task_json)
            producer.flush() # Ensure message is sent
            print(f"🎫 [Kafka]: User {user_id} added to queue.")
            return True
        except Exception as e:
            print(f"❌ [Error]: Queue Failed. {e}")
            return False

    def process_queue(self, ai_worker_function):
        """
        CONSUMER: Worker (AI) yahan se kaam uthata hai.
        Infinite loop jo background mein chalta rahega.
        """
        # Consumer settings update
        consumer_conf = self.conf.copy()
        consumer_conf.update({
            'group.id': 'a1_worker_group',
            'auto.offset.reset': 'earliest'
        })
        
        consumer = Consumer(consumer_conf)
        consumer.subscribe([self.topic])
        
        print("👷 [Worker]: Waiting for tasks...")
        
        try:
            while True:
                msg = consumer.poll(1.0) # 1 second wait
                
                if msg is None:
                    continue
                if msg.error():
                    print(f"⚠️ [Kafka Error]: {msg.error()}")
                    continue

                # Process the Task
                data = json.loads(msg.value().decode('utf-8'))
                print(f"⚙️ [Worker]: Processing task for User {data['user']}...")
                
                # Yahan actual AI kaam karega
                ai_worker_function(data['task'])
                
                print(f"✅ [Worker]: Task Complete.")
                
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

# --- Configuration Template (Example) ---
# conf = {
#     'bootstrap.servers': 'falsely-promoted-condor-xxxxx.upstash.io:9092',
#     'security.protocol': 'SASL_SSL',
#     'sasl.mechanisms': 'SCRAM-SHA-256',
#     'sasl.username': 'your_username',
#     'sasl.password': 'your_password'
# }
