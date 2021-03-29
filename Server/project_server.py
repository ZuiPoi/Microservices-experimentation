import grpc
from concurrent import futures
import time
import os
import pandas as pd
import project_pb2_grpc as pb2_grpc
import project_pb2 as pb2


class StreamService(pb2_grpc.StreamServiceServicer):

    def __init__(self, *args, **kwargs):
        pass

    def FetchResponse(self, request, context):
        x = take_input_data()
        post = pb2.streamResponse()
        i=0
        while i<len(x):
                post.postid = str(x.iloc[i]['id'])
                post.title = str(x.iloc[i]['title'])
                post.score = int(x.iloc[i]['score'])
                post.author = str(x.iloc[i]['author'])
                post.removed = str(x.iloc[i]['removed_by'])
                post.total_awards = int(x.iloc[i]['total_awards_received'])
                post.awarders = str(x.iloc[i]['awarders'])
                post.created_utc = str(x.iloc[i]['created_utc'])
                post.full_link = str(x.iloc[i]['full_link'])
                post.num_comments = int(x.iloc[i]['num_comments'])
                post.over_18 = str(x.iloc[i]['over_18'])
                yield post
                time.sleep(0.5)
                i=i+1




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_StreamServiceServicer_to_server(StreamService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("server started")
    server.wait_for_termination()


def read_line(line):
    res = ()
    list_params = line.strip().split(",")
    if list_params[0] != "id":
        if (len(list_params) > 0):
            list_params[2] = int(list_params[2])
            if(list_params[4] == ""):
                list_params[4] = "none"
            if (list_params[5] == ""):
                list_params[5] = "unknown"
            if (list_params[6] == ""):
                list_params[6] = 0
            elif (list_params[6] == "0.0"):
                list_params[6] = 0
            else:
                list_params[6] = int(list_params[6])

            if (list_params[7] == ""):
                list_params[7] = "[]"

            list_params[10] = int(list_params[10])

            res = tuple(list_params)

    return res

def take_input_data():
    input_file = "./data/r_dataisbeautiful_posts.csv"
    data = pd.read_csv(input_file, dtype={"removed_by": "string","awarders": "string" })
    my_series = data.squeeze()
   # print(my_series)
    return data

if __name__ == '__main__':
    x =take_input_data()
    i = 0
    #while i < len(x):
     #   print((x.iloc[[i], [0]]).to_string(index=False))
     #   i=i+1
    serve()