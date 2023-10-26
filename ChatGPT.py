import json
from datetime import datetime, timedelta

import requests

def cloudbypass(type, url, headers=None, data=None):
      # 将url中的域名替换为api.cloudbypass.com
      url = url.replace("https://chat.openai.com", "https://api.cloudbypass.com")
      headers['x-cb-apikey'] = '0afb3d545e274d04ab6fd88e6dafcd2b'
      headers['x-cb-host'] = 'chat.openai.com'

      response = requests.request(type, url, headers=headers, data=data)
      return response

class ChatGPT:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://chat.openai.com"
        self.headers = {
              'authority': 'chat.openai.com',
              'accept': '*/*',
              'accept-language': 'en-US',
              'authorization': 'Bearer ' + self.token,
              'sec-fetch-site': 'same-origin',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
        }



    def conversation(self, id):
        url = f"{self.base_url}/backend-api/conversation/{id}"
        response = cloudbypass("GET", url, headers=self.headers)
        return response.json()

    def conversation_text(self, id):
        data = self.conversation(id)
        if 'mapping' not in data:
            print(data)
            return json.dumps(data, indent=4)
        mapping = data['mapping']

        # 初始化一个空列表来存储对话
        conversation = []

        # 遍历映射表
        for node_id, node_data in mapping.items():
            # 检查'message'键是否存在
            if 'message' in node_data:
                try:
                    message_data = node_data['message']
                    author = message_data['author']['role']
                    content = message_data['content']['parts'][0]
                except:
                    # 打印错误
                    print(json.dumps(node_data['message'], indent=4))
                    continue
                conversation.append(f"# {author}: \n{content}")

        # 输出对话
        return "\n".join(conversation)

    def conversation_json(self, id):
        data = self.conversation(id)

        mapping = data['mapping']

        # 初始化一个空列表来存储对话
        conversation = []

        # 遍历映射表
        for node_id, node_data in mapping.items():
            # 检查'message'键是否存在
            if 'message' in node_data:
                message_data = node_data['message']
                author = message_data['author']['role']
                content = message_data['content']['parts'][0]
                # 检查'create_time'键是否存在，如果不存在，则使用默认值
                timestamp = message_data.get('create_time', data.get('create_time', 0))
                # 将Unix时间戳转换为可读的日期时间格式，或使用'Unknown'作为默认值
                if timestamp != 0:
                    # 为时间添加8小时的偏移以转换为本地时间
                    local_datetime = datetime.utcfromtimestamp(timestamp) + timedelta(hours=8)
                    time_str = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    time_str = 'Unknown'
                # 创建一个字典来存储消息的详细信息
                message_info = {
                    'author': author,
                    'content': content,
                    'time': time_str
                }
                # 将消息的详细信息添加到对话列表中
                conversation.append(message_info)

        # 创建一个新的JSON对象来存储对话
        output_data = {
            'title': data['title'],
            'conversation': conversation
        }
        return output_data

        # # 将输出数据转换为JSON字符串，并打印到控制台
        # output_json = json.dumps(output_data, indent=2, ensure_ascii=False)
        # print(output_json)




if __name__ == '__main__':
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJnbHdoYXBwZW5Ab3V0bG9vay5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJwb2lkIjoib3JnLXJTYW9tenhoeUR4QlZVMjJiOUdFSmFDNSIsInVzZXJfaWQiOiJ1c2VyLXRwN2dKZXpQdkhvbVBZQWJZczRwU0h3ZSJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiYXV0aDB8NjQ3NzZiODE1MjBiODhhMTNhZTI1NGQ2IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5NzQyMDUwNSwiZXhwIjoxNjk4Mjg0NTA1LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSBvZmZsaW5lX2FjY2VzcyJ9.M-RrOBLOpq_8qLK-Qk7NhCDorOv-UEYd7CiX8oVybsgblQDjOwouOKaCodcgpTK5ytFVg82SMyt0IBaKULaXlh-MJzz9Xy5rvfOwheudvyZQx19u9dJbN9BxkhvOz0Yki9bOEw0Vs3cK4yUPBXpwuIw81tfPqGCQl4yXojis9P3qVeWqZKYV9gEyaQ5LPWgZ-4cG7WRMK6q2KAMoYEvCO-bOU8xsAxfuwfpzCXAd1NmMckvbzvBjWQgfg2IJlQM1lyxjkgUXYFIXkela4F5RR-N5pXdTSBv2r0seJSUv3Iv3Yxyb7TQo4mlRzj56NlLcSvC8GGnJr0uZ0WO2-mshBg"
    chat = ChatGPT(token)
    data = chat.conversation_text("7fd937cc-fa80-4f29-bca7-100b85932c3b")
    print(data)